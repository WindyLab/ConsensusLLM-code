import re
import numpy as np
from .gpt import GPT
from ..prompt.summarize import summarizer_role
from ..prompt.form import summarizer_output_form

class Agent2D(GPT):
  # TODO:Construct a 'Robot' class that inherits from the 'Agent' class.
  def __init__(self, position, other_position, key: str, name=None,
               model: str = 'gpt-3.5-turbo-0613', temperature: float = 0.7, keep_memory=False):
    super().__init__(key=key, model=model, temperature=temperature, keep_memory=keep_memory)
    self.__name = name
    self.__velocity = np.zeros(2)  # Current velocity of the agent
    self.__max_traction_force = 50  # Maximum traction force of the agent (N)
    self.__max_velocity = 3  # Maximum velocity of the agent (m/s)
    self.__m = 15  # Mass of the agent (kg)
    self.__mu = 0.02  # Friction coefficient
    # PID Parameters
    self.Kp = np.array([1.2, 1.2], dtype=np.float64)
    self.Ki = np.array([0.0, 0.0], dtype=np.float64)
    self.Kd = np.array([6, 6], dtype=np.float64)
    self.prev_error = np.array([0, 0], dtype=np.float64)
    self.integral = np.array([0, 0], dtype=np.float64)
    self.__target_position = None  # Target position of the agent
    self.__position = position  # Current position of the agent
    self.__other_position = other_position  # Positions of other agents
    self.__trajectory = []  # Record the agent's movement trajectory
    self.__target_trajectory = []  # Record the agent's target trajectory
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

  @property
  def trajectory(self):
    return self.__trajectory

  @property
  def target_trajectory(self):
    return self.__target_trajectory

  @property
  def target_position(self):
    return self.__target_position

  @other_position.setter
  def other_position(self, value):
    self.__other_position = value

  @property
  def summarize_result(self):
    return self.__summarize_result

  def answer(self, input, idx, round, simulation_ind, try_times=0) -> tuple:
    try:
      answer = self.generate_answer(input=input, try_times=try_times)
      self.__target_position = self.parse_output(answer)
      self.__target_trajectory.append(self.__target_position)
      return idx, self.__target_position
    except Exception as e:
      try_times += 1
      if try_times < 3:
        print(
          f"An error occurred when agent {self.__name} tried to generate answers: {e},try_times: {try_times + 1}/3.")
        return self.answer(input=input, idx=idx, round=round, simulation_ind=simulation_ind, try_times=try_times)
      else:
        print(f"After three attempts, the error still remains unresolved, the input is:\n'{input}'\n.")
        return idx, self.__target_position

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
    matches = re.findall(r'\((.*?)\)', output)
    if matches:
      last_match = matches[-1]
      numbers = re.findall(r'[-+]?\d*\.\d+|\d+', last_match)
      if len(numbers) == 2:
        x = float(numbers[0])
        y = float(numbers[1])
        return (x, y)
      else:
        raise ValueError(f"The last match {last_match} does not contain exactly 2 numbers.")
    else:
      raise ValueError(f"No array found in the output: \n{output}")

  def move(self, time_duration: float):
    if self.__target_position is None:
      print("Target not set!")
      return
    error = np.array(self.__target_position) - np.array(self.__position)
    self.integral += error * time_duration
    derivative = (error - self.prev_error) / time_duration
    force = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
    force_magnitude = np.linalg.norm(force)
    if force_magnitude > self.__max_traction_force:
      force = (force / force_magnitude) * self.__max_traction_force
    # friction_force = -self.__mu * self.__m * 9.8 * np.sign(self.__velocity) if abs(
    #   np.linalg.norm(self.__velocity)) > 0.1 else 0
    friction_force = 0
    net_force = force + friction_force
    acceleration = net_force / self.__m
    self.__velocity += acceleration * time_duration
    # Limit the velocity
    velocity_magnitude = np.linalg.norm(self.__velocity)
    if velocity_magnitude > self.__max_velocity:
      self.__velocity = (self.__velocity / velocity_magnitude) * self.__max_velocity
    self.__position += self.__velocity * time_duration + 0.5 * acceleration * time_duration ** 2
    self.__position = tuple(np.round(self.__position, 2))
    self.prev_error = error
    self.__trajectory.append(self.__position)
    # print(
    #   f"{self.__name} position: {self.__position}, target: {self.__target_position}, velocity: {self.__velocity}, force: {force}, friction_force: {friction_force}, net_force: {net_force}, acceleration: {acceleration}")
    return self.__position