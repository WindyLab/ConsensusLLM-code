# Multi-agent consensus seeking via LLM

<p align="center">
  <a href="https://github.com/WestlakeIntelligentRobotics/consensus-seeking-llm">
    <img src="https://img.shields.io/badge/arXiv-paper?style=socia&logo=arxiv&logoColor=white&labelColor=grey&color=blue"></a>
  <a href="https://github.com/WestlakeIntelligentRobotics/consensus-seeking-llm">
    <img src="https://img.shields.io/badge/Paper-blue?logo=googledocs&logoColor=white&labelColor=grey&color=blue"></a>
  <a href="https://github.com/WestlakeIntelligentRobotics/consensus-seeking-llm">
    <img src="https://img.shields.io/badge/Website-blue?logo=semanticweb&logoColor=white&labelColor=grey&color=blue"></a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white&labelColor=grey&color=blue"></a>
</p>

Multi-agent systems driven by large language models (LLMs) have shown promising abilities for solving complex tasks in a collaborative manner. This work addresses *consensus seeking*, which is a fundamental problem for collective decision-making systems. In particular, when multiple LLMs work together, we are interested in how they can reach a consensus through inter-agent negotiation given that they have different initial solutions/opinions about a task. To that end, this work studies an abstract consensus-seeking task, where the state of each LLM-driven agent is a numerical number and they negotiate with each other to reach a consensus value. We found that when not explicitly directed on which strategy should be adopted, the LLMs tend to use the *average strategy* for consensus seeking although they may use some other strategies occasionally. Moreover, this work analyzes the impact of agents' *personalities* and *network topologies* on the negotiation process. It is shown that stubborn agents tend to dominate the consensus outcome, resulting in leader-follower structures, while network topologies can influence the speed and success of consensus convergence. The significance of this work lies in its potential to lay the foundations for understanding the behaviors of LLM-driven multi-agent systems to reach consensus in collaborative problem-solving tasks.


### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: This project is primarily developed in Python. Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- **Python Libraries**: You will need to install several Python libraries to run the code. You can install these libraries using pip, Python's package manager. To install the required libraries, run the following command:

  ```bash
  pip install -r requirements.txt
  ```

  The `requirements.txt` file, included in this repository, lists all the necessary Python libraries along with their versions.

- **Docker (Optional)**: If you plan to deploy the project using Docker, you'll need to have Docker installed on your system. 

  1. You can download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop).

  2. **Build the Docker Image:**

     To build a Docker image from the included Dockerfile, navigate to the project directory in your terminal and run the following command:

     ```bash
     docker build -t consensus-debate .
     ```

     This command will create a Docker image named `my-project-image` using the Dockerfile in the current directory.

  3. **Mounting Your Code:**

     You can mount your code into the Docker container by using the `-v` option when running the container. For example:

     ```bash
     docker run -it -p -v /path/to/your/code:/data consensus-debate /bin/bash
     ```

     Replace `/path/to/your/code` with the absolute path to your project directory. The `-v` flag maps your local code directory to the `/data` directory inside the Docker container.

- **OpenAI API Keys:**

  You will need valid OpenAI API keys to interact with the OpenAI services. Follow these steps to add your API keys to the `config.yml` file:

  1. Create a `config/keys.yml` file in the root directory of the project if it doesn't already exist.

  2. Open the `config/keys.yml` file with a text editor.

  3. Add your API keys in the following format, replacing the placeholder keys with your actual OpenAI API keys:

     ```yaml
     api_keys:
       0: "sk-YourFirstAPIKeyHere"
       1: "sk-YourSecondAPIKeyHere"
       2: "sk-YourThirdAPIKeyHere"
     ```

     You can add multiple API keys as needed, and they will be accessible by index.

  4. Set the `api_base` value to the OpenAI API endpoint:

     ```yaml
     api_base: 'https://api.openai.com/v1'
     ```

  5. Save and close the `config.yml` file.

By ensuring you have these prerequisites in place, you'll be ready to use the code and run the experiments described in this project.

### Running Experiments

1. **Create Test Files**: In the "test" directory, create one or more Python test files (e.g., `my_experiment.py`) that define the experiments you want to run. These test files should import and use your Python template as a framework for conducting experiments. Below is an example of what a test file might look like:

   ```python
   import datetime
   import subprocess
   
   def main(n_agent):
     rounds = 9 # number of rounds in single experiment
     agents = n_agent
     n_stubborn = 0 # number of stubborn agents
     n_suggestible = 0 # number of suggestible agents
     n_exp = 9 # number of experiments
     current_datetime = datetime.datetime.now()
     # Format the date as a string
     formatted_date = current_datetime.strftime("%Y-%m-%d_%H-%M")
     out_file = "./log/scalar_debate/n_agents{}_rounds{}_n_exp{}_{}".format(agents, rounds, n_exp, formatted_date)
     # Build the command line
     cmd = [
       'python', './run.py',
       '--rounds', str(rounds),
       '--out_file', out_file,
       '--agents', str(agents),
       '--n_stubborn', str(n_stubborn),
       '--n_suggestible', str(n_suggestible),
       '--n_exp', str(n_exp),
       # '--not_full_connected' # uncomment this if you want use other topology structures
     ]
   
     # Run the command
     subprocess.run(cmd)
   
   if __name__ == "__main__":
     main(n_agent=3)
   ```

   Customize the experiment setup according to your specific needs.

2. **Run Experiments**: You can run the experiments from the command line by executing the test files in the root directory:

   ```bash
   python test/my_experiment.py
   ```

   Replace `my_experiment.py` with the name of the test file you want to run. This will execute your experiment using the Python template and generate results accordingly.

### Results

After running experiments using the provided test files, you can find the data files and logs in the "log" directory. The "log" directory is defined in your test files, and it's where your experiment results  are stored.

### Plotting and Generating HTML

#### Plotting Data

The code includes functionality for automatic plotting of data when running experiments. However, if you wish to manually plot a specific data file, you can use the following command:

```bash
python -m modules.visual.plot ./log/scalar_debate_temp_0_7/n_agents8_rounds9_n_exp9_2023-10-11_13-44/data.p
```

Replace the file path (`./log/scalar_debate_temp_0_7/n_agents8_rounds9_n_exp9_2023-10-11_13-44/data.p`) with the path to the specific data file you want to plot. This command will generate plots based on the provided data file.

#### Generating HTML Reports

The code automatically generates HTML reports for experiments. However, if you want to manually generate an HTML report for a specific experiment or dataset, you can use the following command:

```bash
python ./gen_html.py
```

This command will generate an HTML report based on the data and logs available in the "log" directory.

Please note that for automatically generated HTML reports, the script may take into account the latest experiment data and log files available in the "log" directory. However, running `gen_html.py` manually allows you to create an HTML report at any time, independently of experiment execution.

Customize the instructions and file paths in the examples to match the structure and conventions of your project.

### License

[Specify the project's license and any usage terms or restrictions.]
