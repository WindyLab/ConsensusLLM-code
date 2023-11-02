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

import openai

class GPT:
    """
    Initialize the GPT class for interacting with OpenAI's GPT model.
    GPT provides basic methods for interacting with the model and parsing its
    output.
    """

    def __init__(self, key: str, model: str = 'gpt-3.5-turbo-0613',
                 temperature: float = 0.7, keep_memory: bool = True):
        """
        Initialize the GPT class.

        Args:
            key (str): OpenAI API key.
            model (str): The model to use (default: gpt-3.5-turbo-0613).
            temperature (float): Temperature for text generation (default: 0.7).
            keep_memory (bool): Whether to retain memories (default: True).
        """
        self._model = model
        self._openai_key = key
        self._cost = 0
        self._memories = []
        self._keep_memory = keep_memory
        self._temperature = temperature
        self._history = []

    def get_memories(self):
        """
        Get the current memories.

        Returns:
            list: List of memories.
        """
        return self._memories

    def get_history(self):
        """
        Get the conversation history.

        Returns:
            list: List of conversation history.
        """
        return self._history

    def memories_update(self, role: str, content: str):
        """
        Update memories to set roles (system, user, assistant) and content,
        forming a complete memory.

        Args:
            role (str): Role (system, user, assistant).
            content (str): Content.

        Raises:
            ValueError: If an unrecognized role is provided or if roles are
            added in an incorrect sequence.
        """
        if role not in ["system", "user", "assistant"]:
            raise ValueError(f"Unrecognized role: {role}")

        if role == "system" and len(self._memories) > 0:
            raise ValueError('System role can only be added when memories are '
                             'empty')
        if (role == "user" and len(self._memories) > 0 and
            self._memories[-1]["role"] == "user"):
            raise ValueError('User role can only be added if the previous '
                             'round was a system or assistant role')
        if (role == "assistant" and len(self._memories) > 0 and
            self._memories[-1]["role"] != "user"):
            raise ValueError('Assistant role can only be added if the previous '
                             'round was a user role')
        self._memories.append({"role": role, "content": content})
        self._history.append({"role": role, "content": content})

    def generate_answer(self, input: str, try_times=0, **kwargs) -> str:
        """
        Interact with the GPT model and generate an answer.

        Args:
            input (str): Prompt or user input.
            try_times (int): Number of attempts (default is 0).
            kwargs: Additional parameters for the model.

        Returns:
            str: Text-based output result.

        Raises:
            ConnectionError: If there's an error in generating the answer.
        """
        if not self._keep_memory:
            self._memories = [self._memories[0]]

        if try_times == 0:
            self._memories.append({"role": "user", "content": input})
            self._history.append({"role": "user", "content": input})
        else:
            if self._memories[-1]["role"] == "assistant":
                self._memories = self._memories[:-1]

        openai.api_key = self._openai_key

        try:
            response = openai.ChatCompletion.create(
                model=self._model,
                messages=self._memories,
                temperature=self._temperature,
                **kwargs
            )
            self._cost += response['usage']["total_tokens"]
            content = response['choices'][0]['message']['content']
            self._memories.append({"role": "assistant", "content": content})
            self._history.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            raise ConnectionError(f"Error in generate_answer: {e}")
