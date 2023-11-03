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

import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import glob
from .read_data import read_from_file

def extract_data_from_file(file):
    """
    Extract data from a file.

    Args:
        file (str): The file path to read data from.

    Returns:
        numpy.ndarray: A NumPy array containing the extracted data.

    Raises:
        Exception: If an error occurs during data extraction.

    This function reads data from a file, filters it, calculates bias, and 
    returns a NumPy array.
    """
    results = read_from_file(file)
    try:
        # Filter results ensuring each inner list is of length 10 and contains no None values
        filtered_results = [
            mid_list for mid_list in results 
            if all(len(inner_list) == 10 for inner_list in mid_list) 
                and all(item is not None 
                    for inner_list in mid_list 
                    for item in inner_list)
        ]

        # Convert the filtered results to a numpy array for further processing
        filtered_results = np.array(filtered_results)

    except Exception as e:
        print('ERROR:--' + file)
        return []

    bias = []
    # Process each agent's results
    for agent_results in filtered_results:
        # Extract the last value from each result and sort them
        last_values = sorted([res[-1] for res in agent_results])

        # Calculate the mean difference between consecutive sorted last values
        differences = np.mean([last_values[i + 1] - last_values[i] 
                               for i in range(len(last_values) - 1)])

        # If the mean difference is less than 1, compute the bias for each result of the agent
        if differences < 1:
            agent_bias = [res[-1] - res[0] for res in agent_results]
            bias.append(agent_bias)

    # Calculate the mean bias for all agents
    data = np.mean(bias, axis=1)
    return data

def get_data_files(dir, directory_pattern):
    """
    Get data files from a directory based on a directory pattern.

    Args:
        dir (str): The directory to search for data files.
        directory_pattern (str): The pattern to match subdirectories.

    Returns:
        list: A list of file paths.

    This function searches for data files in a directory based on the provided 
    pattern and returns their paths.
    """
    file_paths = []
    for directory in glob.glob(os.path.join(dir, directory_pattern)):
        data_file_path = os.path.join(directory, 'data.p')
        if os.path.isfile(data_file_path):
            file_paths.append(data_file_path)
    return file_paths

def extract_data_from_files(files):
    """
    Extract data from a list of data files.

    Args:
        files (list): A list of data file paths.

    Returns:
        list: A list of extracted data.

    This function extracts data from a list of data files and accumulates it, 
    returning the extracted data.
    """
    data_list = []

    for file in files:
        data_list.extend(extract_data_from_file(file))

        # Check if the length of the accumulated data list is at least 300
        if len(data_list) >= 300:
            print(len(data_list))
            return data_list

# Create a data structure to store results
def plot_result(data):
    """
    Plot the results as a box plot.

    Args:
        data (list): A list of data to be plotted.

    This function creates a box plot to visualize the data.
    """
    plt.boxplot(data, labels=['2 Agents', '3 Agents', '4 Agents', '5 Agents'], 
                patch_artist=True,
                boxprops=dict(facecolor='cyan', color='black'),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'),
                medianprops=dict(color='red'))

    plt.xlabel('Agents number')
    plt.ylabel('Values')
    plt.title('Box Plot Example')
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.2)
    plt.show()

def plot_combined_results(data1, data2):
    """
    Plot combined results as box plots with scatter plots.

    Args:
        data1 (list): Data for the first set of box plots.
        data2 (list): Data for the second set of box plots.

    This function creates combined box plots with scatter plots to compare 
    two datasets.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Define colors
    color_primary_full = (246 / 255, 111 / 255, 106 / 255, 1)
    color_secondary_full = (4 / 255, 183 / 255, 188 / 255, 1)
    color_primary_translucent = (246 / 255, 111 / 255, 106 / 255, 0.7)
    color_secondary_translucent = (4 / 255, 183 / 255, 188 / 255, 0.7)

    # Define box properties
    box_properties_data1 = dict(facecolor=color_secondary_translucent, 
                                color='black')
    box_properties_data2 = dict(facecolor=color_primary_translucent, 
                                color='black')

    # Plot boxplots for data1
    box_plot_data1 = ax.boxplot(
        data1, 
        positions=np.array(range(len(data1))) * 2.0 - 0.4, 
        patch_artist=True,
        boxprops=box_properties_data1, 
        whiskerprops=dict(color='black'),
        capprops=dict(color='black'), 
        medianprops=dict(color='red'), 
        widths=0.6, showfliers=False)

    # Plot boxplots for data2
    box_plot_data2 = ax.boxplot(
        data2, 
        positions=np.array(range(len(data2))) * 2.0 + 0.4, 
        patch_artist=True,
        boxprops=box_properties_data2, 
        whiskerprops=dict(color='black'),
        capprops=dict(color='black'), 
        medianprops=dict(color='red'), 
        widths=0.6, showfliers=False)

    # Scatter plot for data1
    for i, data in enumerate(data1):
        y = data
        x = np.random.normal(i * 2.0 - 0.4, 0.030, len(y))
        ax.scatter(x, y, alpha=0.5, edgecolor='black', 
                   facecolor=color_secondary_full, s=15, zorder=2)

    # Scatter plot for data2
    for i, data in enumerate(data2):
        y = data
        x = np.random.normal(i * 2.0 + 0.4, 0.030, len(y))
        ax.scatter(x, y, alpha=0.5, edgecolor='black', 
                   facecolor=color_primary_full, s=15, zorder=2)

    # Set x and y axis labels and ticks
    ax.set_xticks(np.array(range(len(data1))) * 2.0)
    ax.set_xticklabels(['2', '4', '6', '8'])
    ax.set_xlabel('Agent number', fontsize=13)
    ax.set_ylabel('Bias', fontsize=13)
   
