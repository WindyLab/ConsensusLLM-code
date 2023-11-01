import numpy as np
import pickle

from .template import Template
from ..llm.agent_2d import Agent2D
from ..llm.api_key import api_keys
from ..llm.role import names
from ..prompt.form import agent_output_form
from ..prompt.personality import stubborn, suggestible
from ..prompt.scenario_2d import agent_role, game_description, round_description
from ..visual.gen_html import gen_html
from ..visual.plot_2d import plot_xy, video

class Vector2dDebate(Template):
  def __init__(self, args, connectivity_matrix):
    super().__init__(args)
    self.__dt = 0.1
    self.__n_agents = args.agents
    self.__init_input = game_description + "\n\n" + agent_output_form
    self.__round_description = round_description
    self.__positions = [[]] * args.n_exp
    self.__output_file = args.out_file
    self.__n_suggestible = args.n_suggestible
    self.__n_stubborn = args.n_stubborn
    self.__trajectory = {"pos": {}, "target": {}}  # A dictionary for recording agent trajectories

    # np.random.seed(0)
    # Define the connectivity matrix for agent knowledge
    # m(i, j) = 1 means agent i knows the position of anget j
    self.__m = connectivity_matrix
    # safety check
    if args.n_stubborn + args.n_suggestible > self.__n_agents:
      raise ValueError(f"stubborn + suggestible agents is more than {self.__n_agents}")
    if len(api_keys) < self.__n_agents * args.n_exp:
      raise ValueError(f"api_keys is not enough for {self.__n_agents} agents")
    if self.__m.shape[0] != self.__m.shape[1]:
      raise ValueError(f"connectivity_matrix is not a square matrix, shape: {self.__m.shape}")
    if self.__m.shape[0] != self.__n_agents:
      raise ValueError(f"connectivity_matrix is not enough for {self.__n_agents} agents, shape: {self.__m.shape}")
    
  def generate_agents(self, simulation_ind):
    agents = []
    position = np.array([[20, 20], [80, 20], [50, 80]]) + np.random.randint(-10, 10, size=(self.__n_agents, 2))
    # position = np.random.randint(0, 100, size=(self.__n_agents, 2))

    for idx in range(self.__n_agents):
      position_others = [(x, y) for x, y in position[self.__m[idx, :]]]
      # Create agent instances
      agent = Agent2D(position=tuple(position[idx]),
                    other_position=position_others,
                    key=api_keys[simulation_ind * self.__n_agents + idx],
                    model="gpt-3.5-turbo-0613",
                    name=names[idx])
      # add personality, neutral by default
      personality = ""
      if idx < self.__n_stubborn:
        personality = stubborn
      elif self.__n_stubborn <= idx < self.__n_stubborn + self.__n_suggestible:
        personality = suggestible
      agent.memories_update(role='system',
                            content=agent_role + personality)
      agents.append(agent)
    self.__positions[simulation_ind] = position
    return agents

  def generate_question(self, agent, round) -> str:
    input = self.__init_input.format(agent.position, agent.other_position)
    return input

  def exp_postprocess(self):
    is_success, filename = self.save_record(self.__output_file)
    if(is_success):
      # Call functions to plot and generate HTML
      trajectory_file = self.__output_file + '/trajectory.p'
      plot_xy(trajectory_file)
      video(trajectory_file)
      gen_html(filename, self.__output_file)

  def round_postprocess(self, simulation_ind, round, results, agents):
    origin_result = []
    for i in range(int(2 / self.__dt)):
      for agent in agents:
        agent.move(self.__dt)
        if i == int(2 / self.__dt) - 1:
          origin_result.append(agent.position)
    for idx, agent in enumerate(agents):
      res_filtered = np.array(origin_result)[self.__m[idx, :]]
      other_position = [tuple(x) for x in res_filtered]
      agent.other_position = other_position
    # print("simulation {} round {} finished".format(simulation_ind, round))


  def update_record(self, record, agent_contexts, simulation_ind, agents):
    record[tuple(tuple(pos) for pos in self.__positions[simulation_ind])] = agent_contexts
    self.__trajectory['pos'][simulation_ind] = [agent.trajectory for agent in agents]
    self.__trajectory['target'][simulation_ind] = [agent.target_trajectory for agent in agents]

  def save_record(self, output_dir: str):
    res = super().save_record(output_dir)
    try:
      data_file_trajectory = output_dir + '/trajectory.p'
      pickle.dump(self.__trajectory, open(data_file_trajectory, "wb"))
    except Exception as e:
      print("Error saving trajectory")
      pickle.dump(self.__trajectory, open("trajectory.p", "wb"))
    return res