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

import pickle
import re

def parse_answer(sentence):
    """
    Parses a sentence to extract a floating-point number.

    Args:
        sentence (str): The input sentence to parse.

    Returns:
        float or None: The last floating-point number found in the sentence, 
        or None if none is found.
    """
    floats = re.findall(r'[-+]?\d*\.\d+|\d+', sentence)
    if floats:
        return float(floats[-1])
    else:
        return None

def parse_p_file(filename):
    """
    Parses a Pickle file and returns its content.

    Args:
        filename (str): The name of the Pickle file to parse.

    Returns:
        object: The content of the Pickle file.
    """
    objects = []
    with open(filename, "rb") as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects[0]

def read_conversations(filename):
    """
    Reads conversations from a Pickle file and extracts them.

    Args:
        filename (str): The name of the Pickle file containing conversations.

    Returns:
        list: A list of conversation objects.
    """
    object = parse_p_file(filename)
    conversations = [value for key, value in object.items()]
    return conversations

def read_from_file(filename):
    """
    Reads and extracts data from a Pickle file containing text conversations.

    Args:
        filename (str): The name of the Pickle file containing text 
        conversations.

    Returns:
        list: A list of text answers extracted from the file.
    """
    object = parse_p_file(filename)
    final_ans = []
    count = 0
    for key, value in object.items():
        text_answers = []
        agent_contexts = value
        count += 1
        for agent_id, agent_context in enumerate(agent_contexts):
            ans = [key[agent_id]]
            for i, msg in enumerate(agent_context):
                if i > 0 and i % 2 == 0:
                    text_answer = agent_context[i]['content']
                    text_answer = text_answer.replace(",", ".")
                    text_answer = parse_answer(text_answer)
                    ans.append(text_answer)
            text_answers.append(ans)
        final_ans.append(text_answers)
    return final_ans

if __name__ == "__main__":
    res = """Based on the advice of your two friends, the position to meet your 
    friend is 65.5, which is the midpoint of your position (64) and your 
    friend's position (67). Therefore, the position to meet your 
    friend is 65.."""
    print(parse_answer(res))
