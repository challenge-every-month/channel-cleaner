import os
import json

with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
    config_json = json.load(config_file)
    os.environ['slack_token'] = config_json['token']
    print({f"token:{config_json['token']}"})
    os.environ['slack_channel_id'] = config_json['channel_id']
