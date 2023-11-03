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

from modules.visual.util import render_conversations_to_html
from modules.visual.read_data import read_from_file, read_conversations
import os
import sys

def gen_html(data_path, html_dir):
    """
    Generate HTML output for conversations.

    Args:
        data_path (str): The path to the data file.
        html_dir (str): The directory to save the generated HTML files.

    Generates HTML output for the conversations and saves them in the 
    specified directory.
    """
    results = read_conversations(data_path)

    for ind, res in enumerate(results):
        output_file = os.path.join(html_dir, f'simulation_{ind}.html')
        if os.path.exists(output_file):
            continue
        try:
            render_conversations_to_html(res, output_file, ind)
            print(f'HTML output has been written to {output_file}')
        except:
            continue

if __name__ == "__main__":
    log_directory = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    category = 'log/scalar_debate/n_agents3_rounds9_n_exp3_2023-10-07_16-38.p'
    directory_path = os.path.join(log_directory, category)

    files = [os.path.join(directory_path, file) 
             for file in os.listdir(directory_path) 
             if os.path.isfile(os.path.join(directory_path, file))]

    for file in files:
        if file.endswith(".p"):
            gen_html(file, directory_path)
