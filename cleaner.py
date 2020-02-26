import json
import time
from datetime import datetime
from slack_api import SlackApi

with open('config.json') as config_file:
    config_json = json.load(config_file)
    api = SlackApi(config_json)
    TIMELIMIT = float(config_json.get('time_limit', 12)) * 3600


def clean():

    history = api.history()

    for m in history:
        delta = datetime.now()  - datetime.fromtimestamp(float(m['ts']))
        if delta.seconds >= TIMELIMIT:
            api.delete(float(m['ts']))
            # 連続で送りすぎるとエラーになるので1秒待機
            time.sleep(1)


if __name__ == "__main__":
    clean()
