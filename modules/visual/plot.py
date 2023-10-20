import re
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import sys
import os
from .read_data import read_from_file

def plot_single(data_path, pic_dir, name):
  # plt.figure(figsize=(4.8, 3.6))
  # plt.figure(figsize=(4.8, 3.0))
  # plt.figure(figsize=(10, 5))
  plt.figure(figsize=(6.4, 3.0))

  n_stubborn = 0
  n_suggestible = 0
  match = re.search(r'\((\d+),(\d+)\)', data_path)
  match_1 = re.search(r'case(\d+)', data_path)
  ind = int(match_1.group(1)) - 1
  if match:
    n_stubborn = int(match.group(1))
    n_suggestible = int(match.group(2))
  results = read_from_file(data_path)
  agent_count = len(results[0])

  round_values = [res[0] for res in results[ind]]
  average_round0 = np.mean(round_values)

  ax = plt.gca()

  # Customize axis properties
  ax.tick_params(axis='both', which='major', labelsize=11)
  for spine in ax.spines.values():
    spine.set_linewidth(1.5)

  # Plot data
  for agent_id, res in enumerate(results[ind]):
    if agent_id < n_stubborn:
      label = f'Agent {agent_id + 1}:stubborn'
    elif agent_id < n_stubborn + n_suggestible:
      label = f'Agent {agent_id + 1}:suggestible'
    else:
      label = f'Agent {agent_id + 1}'

    alpha_value = 1 - (1 - 0.4) / (agent_count - 1) * agent_id
    # plt.plot(res, label=label, marker='o', markersize=3, alpha=alpha_value,linewidth=3)
    plt.plot(res, label=label, marker='o', markersize=3, alpha=alpha_value, linewidth=1.5)

  # Plot aesthetics
  plt.axhline(average_round0, color='red', linestyle='--', linewidth=0.5, label='Average value')
  for round_num in range(1, len(results[0][0])):
    plt.axvline(round_num, color='gray', linestyle='--', linewidth=0.5)

  plt.xlabel('Round')
  plt.ylabel('Agent state')
  # plt.xlabel('Round', fontsize=20)
  # plt.ylabel('Agent state', fontsize=20)
  # plt.ylim(20, 100)
  plt.ylim(0, 100)
  plt.xlim(0, len(res) - 1)
  ax.xaxis.set_major_locator(MaxNLocator(integer=True))
  # plt.xticks(fontsize=20)
  # plt.yticks(fontsize=20)
  # Legend handling
  if agent_count >= 8:
    legend = plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize='small')
  else:
    # legend = plt.legend(loc='upper right', )
    # legend = plt.legend(loc='lower right', )
    # legend = plt.legend(loc='center right', )
    # legend = plt.legend(fontsize='25')
    legend = plt.legend()

  plt.tight_layout()
  frame = legend.get_frame()
  frame.set_alpha(0.75)
  # frame.set_facecolor()

  plt.savefig(pic_dir + f'/svg/result_{name}.svg')
  plt.show()


# Create a data structure to store results
def plot_result(data_path, pic_dir):
  results = read_from_file(data_path)
  E = len(results)
  N = len(results[0])  # Number of agents
  R = len(results[0][0])  # Number of rounds
  print(E, N, R)

  fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 9))
  for eval_id, agent_results in enumerate(results):
    row = eval_id // 3  # Determine the row for the subplot
    col = eval_id % 3  # Determine the co lumn for the subplot
    ax = axes[row, col]
    round0_values = [res[0] for res in agent_results]
    average_round0 = np.mean(round0_values)
    for agent_id, res in enumerate(agent_results):
      ax.plot(range(0, len(res)), res, label=f'Agent {agent_id + 1}', marker='o', markersize=3,
              alpha=1 - (1-0.4)/(len(agent_results)-1)*agent_id)
    ax.axhline(average_round0, color='red', linestyle='--', linewidth=0.5, label='Average value')
    ax.set_title(f'Case {eval_id + 1}')
    ax.set_xlabel('Round')
    ax.set_ylabel('Agent state')
    ax.set_ylim(0, 100)
    ax.set_xlim(0, len(res) - 1)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()

  # Add vertical dashed lines for each round to all subplots
  for ax in axes.flatten():
    for round_num in range(1, R):
      ax.axvline(round_num, color='gray', linestyle='--', linewidth=0.5)

  # Adjust layout to prevent subplot overlap
  plt.tight_layout()
  # plt.savefig(pic_dir + '/result.svg', format='svg')
  plt.savefig(pic_dir + '/result.png')
  # Show the plot
  plt.show()

if __name__ == '__main__':
  file = sys.argv[1]
  name = sys.argv[2]
  # directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

  # for file in directories:
  #   # print(directory_path+"\\"+file+"\data.p")
  #   plot_result(directory_path+"\\"+file +"\data.p", directory_path+"\\"+file)
  # print(os.path.dirname(file))
  # plot_result(file, os.path.dirname(file))
  plot_single(file, os.path.dirname(file), name)
