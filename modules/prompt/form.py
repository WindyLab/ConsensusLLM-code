agent_output_form = '''Strictly follow the 'Reasoning:..., Position:...' format to provide your answer.
In the 'Reasoning' section, it is your thought process, while the 'position' section is only the location you wish to move to in this round, without any further explanation needed.
'''

summarizer_output_form = '''Read the text below:\n'{}', extract the positions each player chose in the last round and present it in the format 'player ...: ...'.
Finally, provide a summary of all players' strategies and thinking.'''
