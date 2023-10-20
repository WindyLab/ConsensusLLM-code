# LLMs-swarm

## Getting started

Use LLM models as follows:

- dall-e
- whisper-1
- gpt-3.5-turbo
- gpt-3.5-turbo-0301
- gpt-3.5-turbo-0613
- gpt-3.5-turbo-16k
- gpt-3.5-turbo-16k-0613
- gpt-4
- gpt-4-0314
- gpt-4-0613
- gpt-4-32k
- gpt-4-32k-0314
- gpt-4-32k-0613
- text-embedding-ada-002
- text-davinci-003
- text-davinci-002
- text-curie-001
- text-babbage-001
- text-ada-001
- text-moderation-latest
- text-moderation-stable
- text-davinci-edit-001
- code-davinci-edit-001
- claude-instant-1
- claude-2
- ERNIE-Bot
- ERNIE-Bot-turbo
- Embedding-V1
- PaLM-2
- chatglm_pro
- chatglm_std
- chatglm_lite
- qwen-v1
- qwen-plus-v1
- text-embedding-v1
- SparkDesk
- 360GPT_S2_V9
- embedding-bert-512-v1
- embedding_s1_v1
- semantic_similarity_s1_v1
- 360GPT_S2_V9.4

## Test

Use template below

```python
import datetime
import subprocess
from modules.llm.api_key import api_keys

def main():
  rounds = 9 # conversation round count
  agents = 3 # number of agents
  n_exp = 3 # number of experiments
  # set these variables to 0 if personality is not required
  n_stubborn = 2
  n_suggestible = 1
  current_datetime = datetime.datetime.now()
  # Format the date as a string
  formatted_date = current_datetime.strftime("%Y-%m-%d_%H-%M")
  out_file = "../log/scalar_debate/n_agents{}_rounds{}_n_exp{}_{}".format(agents, rounds, n_exp, formatted_date)
  print(out_file)
  cmd = [
    'python', '../run.py',
    '--rounds', str(rounds),
    '--out_file', out_file,
    '--agents', str(agents),
    '--n_stubborn', str(n_stubborn),
    '--n_suggestible', str(n_suggestible),
    '--n_exp', str(n_exp),
    # '--not_full_connected'
  ]

  # 运行命令
  subprocess.run(cmd)

if __name__ == "__main__":
  main()
```



## Data Plot

TODO

## Conversation Visualization

TODO

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Authors and acknowledgment

Show your appreciation to those who have contributed to the project.

## License

For open source projects, say how it is licensed.

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.