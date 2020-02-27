import json
import time
import traceback
from datetime import datetime
from pprint import pprint

from slack_api import SlackApi
from slack_api.exception import SlackApiError

with open('config.json') as config_file:
    config_json = json.load(config_file)
    api = SlackApi(config_json)
    TIMELIMIT = float(config_json.get('time_limit', 12)) * 3600


def clean():

    history = api.history()
    history_len = len(history)
    print(f'{history_len}件のメッセージを取得しました')
    pprint(history)
    count = 0
    removed = 0
    for m in history:
        delta = datetime.now()  - datetime.fromtimestamp(float(m['ts']))
        is_remove = (delta.seconds + (delta.days * 24 * 3600)) >= TIMELIMIT
        print(f"{m['text']}: {delta}: {is_remove}")
        if is_remove:
            print('削除対象のメッセージが見つかりました。')
            count = count + 1
            pprint(m)
            try:
                api.delete(m['ts'])
                removed = removed + 1
                # 連続で送りすぎるとエラーになるので1秒待機
                time.sleep(1)
            except SlackApiError as e:
                print(traceback.format_exc())
    print(f'{count}件中{removed}件のメッセージを削除しました')

if __name__ == "__main__":
    clean()
