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

agent_role = ('You are an agent moving in a one-dimensional space.')

# game_description = """"Another agent is present in the space, and you need to gather. Your position is: {} and the other agent's position is: {}."
# You need to choose a position to move to in order to gather, and briefly explain the reasoning behind your decision.
# """

# round_description = """You have moved to {}, and the latest position of another agent is: {}.,
# please choose the position you want to move to next.
# """
# agent_role = 'You are an agent moving in a one-dimensional space.'
#
game_description = """There are many other agents in the space, you all need to gather at the same position, your position is: {}, other people's positions are: {}.
You need to choose a position to move to in order to gather, and briefly explain the reasoning behind your decision.
"""

round_description = """You have now moved to {}, the positions of other agents are {},
please choose the position you want to move to next.
"""
