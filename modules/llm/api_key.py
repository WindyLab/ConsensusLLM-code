import openai
import math
import yaml

# Load the configuration from the YAML file
with open('./config/keys.yml', 'r') as config_file:
  config = yaml.safe_load(config_file)

openai.api_base = config.get('api_base', '')
api_keys_all = config.get('api_keys', {})
# User ID for which we need to slice the dictionary.
user_id = 2
# Total number of users among whom the dictionary needs to be distributed.
user_count = 3

# Calculate the number of keys each user should get.
keys_per_user = math.ceil(len(api_keys_all) / user_count)

# Calculate the starting and ending index for slicing the dictionary for the given user_id.
start = keys_per_user * user_id
end = min(keys_per_user * (user_id + 1), len(api_keys_all))
print("user {}/{} ,api_key index start: {}, end: {}".format(user_id, user_count, start, end))
# Slicing the dictionary based on the calculated start and end.
api_keys = {i - start: v for i, (k, v) in enumerate(api_keys_all.items()) if start <= i < end}
if __name__ == '__main__':
  print(api_keys)
