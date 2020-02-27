import json
import time
from pprint import pprint
from datetime import datetime
from slack_api import SlackApi

with open('config.json') as config_file:
    config_json = json.load(config_file)
    api = SlackApi(config_json)
    TIMELIMIT = float(config_json.get('time_limit', 12)) * 3600


def clean():

    history = api.history()
    history_len = len(history)
    print(f'{history_len}件のメッセージを取得しました')
    pprint(history)
    for m in history:
        delta = datetime.now()  - datetime.fromtimestamp(float(m['ts']))
        is_remove = (delta.seconds + (delta.days * 24 * 3600)) >= TIMELIMIT
            print('削除対象のメッセージが見つかりました。')
            pprint(m)
            api.delete(m['ts'])
            # 連続で送りすぎるとエラーになるので1秒待機
            time.sleep(1)


if __name__ == "__main__":
    clean()
