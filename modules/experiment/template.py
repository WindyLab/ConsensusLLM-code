import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pickle
import threading
import queue

# Use template pattern to design a template for different experiments
class Template(ABC):
  def __init__(self, args):
    # Initialize instance variables
    self._record = {}  # A dictionary for recording data
    self._n_agent = args.agents  # Number of agents
    self._n_round = args.rounds  # Number of rounds
    self._n_experiment = args.n_exp  # Number of experiments
    self._lock = threading.Lock()  # Lock for thread safety

  @abstractmethod
  def generate_question(self, agent, round) -> str:
    pass

  @abstractmethod
  def generate_agents(self, simulation_ind):
    pass

  @abstractmethod
  def update_record(self, record, agent_contexts, simulation_ind, agents):
    pass

  @abstractmethod
  def round_postprocess(self, simulation_ind, round, results, agents):
    pass

  @abstractmethod
  def exp_postprocess(self):
    pass

  def run(self):
    try:
      # Use a thread pool to run experiments concurrently
      with ThreadPoolExecutor(max_workers=self._n_experiment) as executor:
        progress = tqdm(total=self._n_experiment * self._n_round, desc="Processing", dynamic_ncols=True)
        futures = {executor.submit(self.run_once, sim_ind, progress) for sim_ind in range(self._n_experiment)}

        for future in as_completed(futures):
          if future.exception() is not None:
            print(f"A thread raised an exception: {future.exception()}")
        progress.close()
    except Exception as e:
      print(f"An exception occurred: {e}")
    finally:
      self.exp_postprocess()

  def run_once(self, simulation_ind, progress):
    agents = self.generate_agents(simulation_ind)
    try:
      for round in range(self._n_round):
        results = queue.Queue()
        n_thread = len(agents) if round < 4 else 1
        # Use a thread pool to run agent tasks concurrently
        with ThreadPoolExecutor(n_thread) as agent_executor:
          futures = []
          for agent_ind, agent in enumerate(agents):
            question = self.generate_question(agent, round)
            futures.append(agent_executor.submit(agent.answer, question, agent_ind, round, simulation_ind))

          for ind, future in enumerate(as_completed(futures)):
            if future.exception() is not None:
              print(f"A thread raised an exception: {future.exception()}")
            else:
              idx, result = future.result()
              results.put((idx, result))
        results = list(results.queue)
        results = sorted(results, key=lambda x: x[0])
        progress.update(1)
        self.round_postprocess(simulation_ind, round, results, agents)

    except Exception as e:
      print(f"error:{e}")
    finally:
      agent_contexts = [agent.get_history() for agent in agents]
      with self._lock:
        self.update_record(self._record, agent_contexts, simulation_ind, agents)

  def save_record(self, output_dir: str):
    try:
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      data_file = output_dir + '/data.p'
      # Save the record to a pickle file
      pickle.dump(self._record, open(data_file, "wb"))
      return True, data_file
    except Exception as e:
      print(f"An exception occurred while saving the file: {e}")
      print("Saving to the current directory instead.")
      # Backup in case of an exception
      pickle.dump(self._record, open("backup_output_file.p", "wb"))
      return False, ""
