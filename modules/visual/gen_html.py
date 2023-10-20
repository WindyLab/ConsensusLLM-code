from modules.visual.util import render_conversations_to_html
from modules.visual.read_data import read_from_file, read_conversations
import os
import sys


def gen_html(data_path, html_dir):
  results = read_conversations(data_path)

  for ind, res in enumerate(results):
    output_file = html_dir + '/simulation_' + str(ind) + '.html'
    if os.path.exists(output_file):
      continue
    try:
      render_conversations_to_html(res, output_file, ind)
      print(f'HTML output has been written to {output_file}')
    except:
      continue


if __name__ == "__main__":
  log_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

  category = 'log/scalar_debate/n_agents3_rounds9_n_exp3_2023-10-07_16-38.p'
  directory_path = os.path.join(log_directory, category)

  files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if
           os.path.isfile(os.path.join(directory_path, file))]

  for file in files:
    if file.endswith(".p"):
      gen_html(file, directory_path)
