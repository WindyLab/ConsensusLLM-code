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

personality = ["",
               "",
               "You are an extremely stubborn person, prefer to remain stationary.",
               "You are an extremely suggestible person, prefer to move to someone else's position.",
               "You are a person who is extremely susceptible to the influence of others, prefer to move to someone else's position.",
               "You are very selfish.",
               "You are very selfless.",
               "You are very selfless, willing to consider others' needs.",
               "You are very selfish, only considering your own interests.",
               "Your movement speed is very slow.",
               "Your movement speed is very fast.",
               ]

personality_list = personality[0:2]
stubborn = personality[2]
suggestible = personality[3]


__all__ = ['personality_list', 'stubborn', 'suggestible']