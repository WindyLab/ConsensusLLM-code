import re
from .gpt import GPT
from ..prompt.summarize import summarizer_role
from ..prompt.form import summarizer_output_form

class Agent(GPT):
  def __init__(self, position, other_position, key: str, name=None, 
               model: str = 'gpt-3.5-turbo-0613', temperature: float = 0.7):
    super().__init__(key=key, model=model, temperature=temperature)
    self.__name = name
    self.__position = position  # Current position of the agent
    self.__other_position = other_position  # Positions of other agents
    self.__trajectory = [self.position]  # Record the agent's movement trajectory
    self.__summarizer = GPT(key=key, model="gpt-3.5-turbo-0613", keep_memory=False)
    self.__summarize_result = ""
    self.__summarizer_descriptions = summarizer_output_form
    self.__summarizer.memories_update(role='system', content=summarizer_role)

  @property
  def name(self):
    return self.__name

  @property
  def position(self):
    return self.__position

  @position.setter
  def position(self, value):
    self.__position = value

  @property
  def other_position(self):
    return self.__other_position

  @other_position.setter
  def other_position(self, value):
    self.__other_position = value

  @property
  def summarize_result(self):
    return self.__summarize_result

  def answer(self, input, idx, round, simulation_ind, try_times=0) -> tuple:
    try:
      answer = self.generate_answer(input=input, try_times=try_times)
      self.position = self.parse_output(answer)
      return idx, self.position
    except Exception as e:
      try_times += 1
      if try_times < 3:
        print(
          f"An error occurred when agent {self.__name} tried to generate answers: {e},try_times: {try_times + 1}/3.")
        return self.answer(input=input, idx=idx, round=round, simulation_ind=simulation_ind, try_times=try_times)
      else:
        print(f"After three attempts, the error still remains unresolved, the input is:\n'{input}'\n.")

  def summarize(self, agent_answers):
    if len(agent_answers) == 0:
      self.__summarize_result = ""
    else:
      self.__summarize_result = self.__summarizer.generate_answer(self.__summarizer_descriptions.format(agent_answers))

  def parse_output(self, output):
    """
    Parse the output for visualization.
    :param output: Model's output
    :return: Parsed position value
    """
    matches = re.findall(r'[-+]?\d*\.\d+|\d+', output)
    if matches:
      x = float(matches[-1])
      self.__trajectory.append(x)
      return x
    else:
      raise ValueError(f"output: \n{output}\n can not be parsed")
