from .scalar_debate import ScalarDebate
from .vector2d_debate import Vector2dDebate

def debate_factory(name, args, connectivity_matrix):
  if(name == "scalar"):
    return ScalarDebate(args, connectivity_matrix)
  elif(name == "2d"):
    return Vector2dDebate(args, connectivity_matrix)
  else:
    return None