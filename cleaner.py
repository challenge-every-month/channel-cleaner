import json
import time
from slack_api import SlackApi

with open('config.json') as config_file:
    api = SlackApi(json.load(config_file))

history = api.history()

for m in history[0]['messages']:
    api.delete(int(m['ts']))
    # 連続で送りすぎるとエラーになるので1秒待機
    time.sleep(1)
