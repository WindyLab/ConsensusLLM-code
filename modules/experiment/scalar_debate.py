"""
MIT License

Copyright (c) [2023] [Intelligent Unmanned Systems Laboratory at 
Westlake University]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM,
OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE, OR OTHER DEALINGS IN
THE SOFTWARE.
"""

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
    """
    A class representing a simulation of scalar debate between multiple agents.

    This class extends the Template class and provides functionality to set up 
    and run a simulation where multiple agents engage in debates, taking into 
    account their positions, personalities, and knowledge connectivity.

    Args:
        args: Command-line arguments and configuration.
        connectivity_matrix: Matrix defining agent knowledge connectivity.

    Raises:
        ValueError: If arguments are invalid or insufficient.
    """
    def __init__(self, args, connectivity_matrix):
        super().__init__(args)
        self._n_agents = args.agents
        self._init_input = game_description + "\n\n" + agent_output_form
        self._round_description = round_description
        self._positions = [[]] * args.n_exp
        self._output_file = args.out_file
        self._n_suggestible = args.n_suggestible
        self._n_stubborn = args.n_stubborn
        np.random.seed(0)

        # Define the connectivity matrix for agent knowledge
        # m(i, j) = 1 means agent i knows the position of agent j
        self._m = connectivity_matrix

        # Safety checks
        if args.n_stubborn + args.n_suggestible > self._n_agents:
            raise ValueError("stubborn + suggestible agents exceed "
                             f"total agents: {self._n_agents}")
        if len(api_keys) < self._n_agents * args.n_exp:
            raise ValueError("api_keys are not enough for "
                             f"{self._n_agents} agents")
        if self._m.shape[0] != self._m.shape[1]:
            raise ValueError("connectivity_matrix is not a square matrix, "
                             f"shape: {self._m.shape}")
        if self._m.shape[0] != self._n_agents:
            raise ValueError("connectivity_matrix size doesn't match the "
                             f"number of agents: {self._m.shape}")

    def generate_agents(self, simulation_ind):
        """
        Generate agent instances based on provided parameters.

        Args:
            simulation_ind: Index of the current simulation.

        Returns:
            List of generated agents.
        """
        agents = []
        position = np.random.randint(0, 100, size=self._n_agents)
        for idx in range(self._n_agents):
            position_others = position[self._m[idx, :]]

            # Create agent instances
            agent = Agent(position=position[idx],
                          other_position=position_others,
                          key=api_keys[simulation_ind * self._n_agents + idx],
                          model="gpt-3.5-turbo-0613",
                          name=names[idx])

            # Add personality, neutral by default
            personality = ""
            if idx < self._n_stubborn:
                personality = stubborn
            elif self._n_stubborn <= idx < (
                self._n_stubborn + self._n_suggestible):
                personality = suggestible
            agent.memories_update(role='system',
                                  content=agent_role + personality)
            agents.append(agent)

        self._positions[simulation_ind] = position
        return agents

    def generate_question(self, agent, round) -> str:
        """
        Generate a question for an agent in a given round.

        Args:
            agent: The agent for which to generate the question.
            round: The current round number.

        Returns:
            A formatted question for the agent.
        """
        if round == 0:
            input = self._init_input.format(agent.position, 
                                            agent.other_position)
        else:
            input = self._round_description.format(agent.position, 
                                                   agent.other_position)
        return input

    def exp_postprocess(self):
        """
        Perform post-processing after the experiment, including saving 
        records and generating plots.
        """
        is_success, filename = self.save_record(self._output_file)
        if is_success:
            # Call functions to plot and generate HTML
            plot_result(filename, self._output_file)
            gen_html(filename, self._output_file)

    def round_postprocess(self, simulation_ind, round, results, agents):
        """
        Perform post-processing for each round of the simulation.

        Args:
            simulation_ind: Index of the current simulation.
            round: The current round number.
            results: Results from the round.
            agents: List of agents.
        """
        for idx, agent in enumerate(agents):
            res_filtered = np.array(results)[self._m[idx, :]]
            other_position = [x for _, x in res_filtered]
            agent.other_position = other_position

    def update_record(self, record, agent_contexts, simulation_ind, agents):
        """
        Update the record with agent contexts for a given simulation.

        Args:
            record: The record to be updated.
            agent_contexts: Contexts of the agents.
            simulation_ind: Index of the current simulation.
            agents: List of agents.
        """
        record[tuple(self._positions[simulation_ind])] = agent_contexts
