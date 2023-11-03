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

import re
from .gpt import GPT
from ..prompt.summarize import summarizer_role
from ..prompt.form import summarizer_output_form

class Agent(GPT):
    """
    A class representing an agent with position control.

    Args:
        position (float): Current position of the agent.
        other_position (list of float): Positions of other agents.
        key (str): API key for the GPT model.
        name (str): Name of the agent (optional).
        model (str): GPT model name (default is 'gpt-3.5-turbo-0613').
        temperature (float): 
            GPT temperature for text generation (default is 0.7).
    """
    def __init__(self, position, other_position, key: str, name=None, 
                 model: str = 'gpt-3.5-turbo-0613', temperature: float = 0.7):
        super().__init__(key=key, model=model, temperature=temperature)
        self._name = name
        self._position = position  # Current position of the agent
        self._other_position = other_position  # Positions of other agents
        self._trajectory = [self.position]  # Record the agent's movement trajectory
        self._summarizer = GPT(key=key, model="gpt-3.5-turbo-0613", 
                               keep_memory=False)
        self._summarize_result = ""
        self._summarizer_descriptions = summarizer_output_form
        self._summarizer.memories_update(role='system', content=summarizer_role)

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def other_position(self):
        return self._other_position

    @other_position.setter
    def other_position(self, value):
        self._other_position = value

    @property
    def summarize_result(self):
        return self._summarize_result

    def answer(self, input, idx, round, simulation_ind, try_times=0) -> tuple:
        """
        Generate an answer using the GPT model.

        Args:
            input (str): Input text or prompt.
            idx: Index.
            round: Round.
            simulation_ind: Simulation index.
            try_times (int): Number of times the answer generation is attempted.

        Returns:
            tuple: Index and the updated position of the agent.
        """
        try:
            answer = self.generate_answer(input=input, try_times=try_times)
            self.position = self.parse_output(answer)
            return idx, self.position
        except Exception as e:
            try_times += 1
            if try_times < 3:
                print(f"An error occurred when agent {self._name} tried to "
                      f"generate answers: {e},try_times: {try_times + 1}/3.")
                return self.answer(input=input, idx=idx, 
                                   round=round, simulation_ind=simulation_ind, 
                                   try_times=try_times)
            else:
                print("After three attempts, the error still remains "
                      f"unresolved, the input is:\n'{input}'\n.")

    def summarize(self, agent_answers):
        """
        Generate a summary of agent answers.

        Args:
            agent_answers (list): List of agent answers.
        """
        if len(agent_answers) == 0:
            self._summarize_result = ""
        else:
            self._summarize_result = self._summarizer.generate_answer(
                self._summarizer_descriptions.format(agent_answers))

    def parse_output(self, output):
        """
        Parse the output for visualization.

        Args:
            output (str): Model's output.

        Returns:
            float: Parsed position value.
        """
        matches = re.findall(r'[-+]?\d*\.\d+|\d+', output)
        if matches:
            x = float(matches[-1])
            self._trajectory.append(x)
            return x
        else:
            raise ValueError(f"output: \n{output}\n can not be parsed")
