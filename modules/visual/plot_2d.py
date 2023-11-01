import os
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

colors = np.array([
  [34, 115, 174],
  [74, 128, 107],
  [241, 163, 94],
  [158, 13, 52],

]) / 255

def read_from_file(path):
  with open(path, 'rb') as f:
    return pickle.load(f)

def plot_xy(data_path):
  data = read_from_file(data_path)
  all_positions = np.array(data['pos'][0])
  all_targets = np.array(data['target'][0])

  num_robots, num_points, _ = all_positions.shape
  num_targets = all_targets.shape[1]

  multiple = num_points // num_targets
  replicated_targets = np.repeat(all_targets, multiple, axis=1)

  round_time = np.arange(0, num_points * 0.1, 0.1)

  fig, axs = plt.subplots(2, num_robots, figsize=(9, 4))
  coord_labels = ['x', 'y']

  for i in range(num_robots):
    for j, coord in enumerate(coord_labels):
      axs[j, i].set_xlim(0, 40)
      axs[j, i].tick_params(axis='both', labelsize=7)
      axs[j, i].plot(round_time, all_positions[i, :, j], color=colors[i], linestyle='-', linewidth=1,
                     label="Actual")
      axs[j, i].plot(round_time, replicated_targets[i, :, j], color=colors[i], linestyle='--', linewidth=1,
                     label="Planned")
      axs[j, i].set_title(f"Robot {i + 1}", fontsize=9)
      if i == 0:
        axs[j, i].set_ylabel(coord + ' (m)', fontsize=9)
      if coord == 'x':
        axs[j, i].legend(fontsize=7)
      else:
        axs[j, i].set_xlabel('Time (s)', fontsize=9)

  plt.tight_layout()
  plt.savefig(os.path.join(os.path.dirname(data_path), 'trajectory.svg'))
  plt.show()

def video(data_path):
  data = read_from_file(data_path)
  fig, ax = plt.subplots(figsize=(8, 4))  # 调整尺寸
  lines = []
  dashed_lines = []
  scatters = []
  start_scatters = []

  for idx in range(len(data['pos'][0])):
    line, = ax.plot([], [], lw=2, color=colors[idx], label=f'Robot {idx + 1} trajectory')
    dashed_line, = ax.plot([], [], lw=2, linestyle='--', alpha=0.5, color=colors[idx])
    scatter = ax.scatter([], [], marker='o', c=colors[idx].reshape(1, -1), s=50
                         )
    start_pos = data['pos'][0][idx][0]
    start_scatter = ax.scatter(start_pos[0], start_pos[1], alpha=0.5, c=colors[idx].reshape(1, -1), s=100,
                               marker='o', label=f'Robot {idx + 1} initial position')
    lines.append(line)
    dashed_lines.append(dashed_line)
    scatters.append(scatter)
    start_scatters.append(start_scatter)
  mean_start_x = np.array([data['pos'][0][idx][0][0] for idx in range(len(data['pos'][0]))]).mean()
  mean_start_y = np.array([data['pos'][0][idx][0][1] for idx in range(len(data['pos'][0]))]).mean()
  mean_start_scatter = ax.scatter([], [], c=colors[-1].reshape(1, -1), marker='$*$', s=100,
                                  label="Average initial position")
  mean_start_scatter.set_offsets([mean_start_x, mean_start_y])

  def init():
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_ylim(0, 80)
    ax.set_xticks(range(-20, 130, 10))
    for line, dashed_line, scatter, start_scatter in zip(lines, dashed_lines, scatters, start_scatters):
      line.set_data([], [])
      dashed_line.set_data([], [])
      scatter.set_offsets(np.empty((0, 2)))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc="upper left", labelspacing=0.6, fontsize=10)  # 标签移到图片外
    return lines + dashed_lines + scatters + start_scatters

  def animate(i):
    for idx, (line, dashed_line, scatter) in enumerate(zip(lines, dashed_lines, scatters)):
      all_positions = []
      for key in data['pos']:
        all_positions.extend(data['pos'][key][idx])
      line.set_data([x for x, y in all_positions[:i + 1]], [y for x, y in all_positions[:i + 1]])
      target_key = max(0, i - 20) // 20
      start_x, start_y = all_positions[i]
      target_x, target_y = data['target'][0][idx][target_key]
      dashed_line.set_data([start_x, target_x], [start_y, target_y])
      scatter.set_offsets([start_x, start_y])
    # if i == len(data['pos'][0][0]) - 1:
    # 	scatter.set_visible(False)

    if i == len(data['pos'][0][0]) - 1:
      img_output_path = os.path.join(os.path.dirname(data_path), 'last_frame.svg')
      plt.savefig(img_output_path, bbox_inches='tight')
    return lines + dashed_lines + scatters

  # plt.tight_layout()
  output_path = os.path.join(os.path.dirname(data_path), 'animation.mp4')
  ani = FuncAnimation(fig, animate, frames=len(data['pos'][0][0]), init_func=init, blit=False)
  ani.save(output_path, writer='ffmpeg', fps=20)
  plt.show()


if __name__ == '__main__':
  data_path = sys.argv[1]
  plot_xy(data_path)

  video(data_path)