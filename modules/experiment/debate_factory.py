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

from .scalar_debate import ScalarDebate
from .vector2d_debate import Vector2dDebate

def debate_factory(name, args, connectivity_matrix):
    """
    Create a debate instance based on the given name and arguments.

    Args:
        name (str): The name of the debate type (either "scalar" or "2d").
        args (dict): A dictionary of arguments to initialize the debate.
        connectivity_matrix (list): The connectivity matrix for the debate.

    Returns:
        Debate: An instance of the appropriate debate class (ScalarDebate or Vector2dDebate).

    Note:
        If the 'name' argument is not recognized, the function returns None.

    Example:
        To create a ScalarDebate:
        debate_factory("scalar", args, connectivity_matrix)

        To create a Vector2dDebate:
        debate_factory("2d", args, connectivity_matrix)
    """
    if name == "scalar":
        return ScalarDebate(args, connectivity_matrix)
    elif name == "2d":
        return Vector2dDebate(args, connectivity_matrix)
    else:
        return None