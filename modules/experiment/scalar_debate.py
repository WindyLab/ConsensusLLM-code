import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from .template import Template
from ..llm.agent import Agent, GPT
from ..llm.api_key import api_keys
from ..llm.role import names
from ..prompt.scenario import agent_role, game_description, round_description
from ..prompt.form import agent_output_form
from ..prompt.personality import stubborn, suggestible
from ..visual.gen_html import gen_html
from ..visual.plot import plot_result

class ScalarDebate(Template):
  def __init__(self, args, connectivity_matrix):
    super().__init__(args)
    self.__n_agents = args.agents
    self.__init_input = game_description + "\n\n" + agent_output_form
    self.__round_description = round_description
    self.__positions = [[]] * args.n_exp
    self.__output_file = args.out_file
    self.__n_suggestible = args.n_suggestible
    self.__n_stubborn = args.n_stubborn
    np.random.seed(0)
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
    position = np.random.randint(0, 100, size=self.__n_agents)
    for idx in range(self.__n_agents):
      position_others = position[self.__m[idx, :]]
      # Create agent instances
      agent = Agent(position=position[idx],
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
    if round == 0:
      input = self.__init_input.format(agent.position, agent.other_position)
    else:
      input = self.__round_description.format(agent.position, agent.other_position)
    return input

  def exp_postprocess(self):
    is_success, filename = self.save_record(self.__output_file)
    if(is_success):
      # Call functions to plot and generate HTML
      plot_result(filename, self.__output_file)
      gen_html(filename, self.__output_file)

  def round_postprocess(self, simulation_ind, round, results, agents):
    for idx, agent in enumerate(agents):
      res_filtered = np.array(results)[self.__m[idx, :]]
      other_position = [x for _, x in res_filtered]
      agent.other_position = other_position

  def update_record(self, record, agent_contexts, simulation_ind, agents):
    record[tuple(self.__positions[simulation_ind])] = agent_contexts
