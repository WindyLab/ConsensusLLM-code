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
    """
    Vector2dDebate is a class that simulates a 2D debate scenario with multiple
    agents.

    This class provides the framework to conduct 2D debates with agents and 
    record their trajectories.

    Args:
        args: 
            An object containing configuration parameters for the debate 
            simulation.
        connectivity_matrix: 
            A square matrix defining agent knowledge connectivity.

    Raises:
        ValueError: 
            If the sum of stubborn and suggestible agents exceeds the total 
            number of agents,
            if there are insufficient API keys for the agents, or if the 
            connectivity matrix is not appropriate.
    """
    def __init__(self, args, connectivity_matrix):
        """
        Initialize the Vector2dDebate instance.

        Args:
            args: An object containing configuration options.
            connectivity_matrix: A matrix defining agent knowledge connectivity.

        Raises:
            ValueError: If the input parameters are invalid.
        """
        super().__init__(args)
        self._dt = 0.1
        self._n_agents = args.agents
        self._init_input = game_description + "\n\n" + agent_output_form
        self._round_description = round_description
        self._positions = [[]] * args.n_exp
        self._output_file = args.out_file
        self._n_suggestible = args.n_suggestible
        self._n_stubborn = args.n_stubborn
        self._trajectory = {"pos": {}, "target": {}}  # A dictionary for recording agent trajectories

        # np.random.seed(0)
        # Define the connectivity matrix for agent knowledge
        # m(i, j) = 1 means agent i knows the position of agent j
        self._m = connectivity_matrix

        # Safety checks for input parameters
        if args.n_stubborn + args.n_suggestible > self._n_agents:
            raise ValueError("stubborn + suggestible agents is more than "
                             f"{self._n_agents}")
        if len(api_keys) < self._n_agents * args.n_exp:
            raise ValueError("api_keys are not enough for "
                             f"{self._n_agents} agents")
        if self._m.shape[0] != self._m.shape[1]:
            raise ValueError("connectivity_matrix is not a square matrix, "
                             f"shape: {self._m.shape}")
        if self._m.shape[0] != self._n_agents:
            raise ValueError("connectivity_matrix is not enough for "
                             f"{self._n_agents} agents, shape: {self._m.shape}")

    def _generate_agents(self, simulation_ind):
        """Generate agent instances for the simulation.

        Args:
            simulation_ind: Index of the simulation.

        Returns:
            List of Agent2D instances.
        """
        agents = []
        position = (np.array([[20, 20], [80, 20], [50, 80]]) 
                    + np.random.randint(-10, 10, size=(self._n_agents, 2)))

        for idx in range(self._n_agents):
            position_others = [(x, y) for x, y in position[self._m[idx, :]]]
            agent = Agent2D(position=tuple(position[idx]),
                            other_position=position_others,
                            key=api_keys[simulation_ind * self._n_agents + idx],
                            model="gpt-3.5-turbo-0613",
                            name=names[idx])
            # add personality, neutral by default
            personality = ""
            if idx < self._n_stubborn:
                personality = stubborn
            elif (self._n_stubborn <= idx 
                  < self._n_stubborn + self._n_suggestible):
                personality = suggestible
            agent.memories_update(role='system', 
                                  content=agent_role + personality)
            agents.append(agent)
        self._positions[simulation_ind] = position
        return agents

    def  _generate_question(self, agent, round) -> str:
        """Generate a question for an agent in a round.

        Args:
            agent: An Agent2D instance.
            round: The current round.

        Returns:
            A formatted string containing the question.
        """
        input = self._init_input.format(agent.position, agent.other_position)
        return input

    def _exp_postprocess(self):
        """Post-process the experiment data, including saving and 
        generating visualizations."""
        is_success, filename = self.save_record(self._output_file)
        if is_success:
            # Call functions to plot and generate HTML
            trajectory_file = self._output_file + '/trajectory.p'
            plot_xy(trajectory_file)
            video(trajectory_file)
            gen_html(filename, self._output_file)

    def _round_postprocess(self, simulation_ind, round, results, agents):
        """Post-process data at the end of each round of the simulation.

        Args:
            simulation_ind: Index of the simulation.
            round: The current round.
            results: Results data.
            agents: List of Agent2D instances.
        """
        origin_result = []
        for i in range(int(2 / self._dt)):
            for agent in agents:
                agent.move(self._dt)
                if i == int(2 / self._dt) - 1:
                    origin_result.append(agent.position)
        for idx, agent in enumerate(agents):
            res_filtered = np.array(origin_result)[self._m[idx, :]]
            other_position = [tuple(x) for x in res_filtered]
            agent.other_position = other_position

    def _update_record(self, record, agent_contexts, simulation_ind, agents):
        """Update the experiment record with agent data.

        Args:
            record: Experiment record data.
            agent_contexts: Contexts of agents.
            simulation_ind: Index of the simulation.
            agents: List of Agent2D instances.
        """
        record[tuple(tuple(pos) for pos in self._positions[simulation_ind])] = (
            agent_contexts)
        self._trajectory['pos'][simulation_ind] = [agent.trajectory 
                                                   for agent in agents]
        self._trajectory['target'][simulation_ind] = [agent.target_trajectory 
                                                      for agent in agents]

    def save_record(self, output_dir: str):
        """Save the experiment record and agent trajectories.

        Args:
            output_dir: Directory where the data will be saved.

        Returns:
            A tuple (is_success, filename).
        """
        res = super().save_record(output_dir)
        try:
            data_file_trajectory = output_dir + '/trajectory.p'
            pickle.dump(self._trajectory, open(data_file_trajectory, "wb"))
        except Exception as e:
            print("Error saving trajectory")
            pickle.dump(self._trajectory, open("trajectory.p", "wb"))
        return res