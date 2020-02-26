import json
import time
from datetime import datetime
from slack_api import SlackApi

with open('config.json') as config_file:
    api = SlackApi(json.load(config_file))

TIMELIMIT = 43200
history = api.history()


def clean():
    for m in history:
        delta = datetime.now()  - datetime.fromtimestamp(float(m['ts']))
        if delta.seconds >= TIMELIMIT:
            api.delete(int(m['ts']))
            # 連続で送りすぎるとエラーになるので1秒待機
            time.sleep(1)


if __name__ == "__main__":
    clean()
