
import time
import traceback
import os
from datetime import datetime
from pprint import pprint
from typing import List, Dict

from slack_api import SlackApi
from slack_api.exception import SlackApiError

api = SlackApi(os.environ['slack_token'], os.environ.get('slack_channel_id'))
TIMELIMIT = float(os.environ.get('time_limit', 12)) * 3600


def filter_message(message: Dict[str, str]):
    message['text'] = None
    message['user'] = None
    message['blocks'] = None
    return message


def select_delete_message(messages: List[Dict[str, str]]) -> List[str]:
    delete_target = []
    for m in messages:
        delta = datetime.now()  - datetime.fromtimestamp(float(m['ts']))
        is_remove = (delta.seconds + (delta.days * 24 * 3600)) >= TIMELIMIT
        print(f"{m['ts']}: {delta}: {is_remove}")
        if is_remove:
            delete_target.append(m['ts'])
            temp = []
            if 'replies' in m:
                for reply in m['replies']:
                    temp.append(reply['ts'])
                delete_target.extend(temp)

    return delete_target


def clean(time_stamps: List[str]) -> int:
    '''
        Args:
            time_stamps:
            [
                1401383885.000061,
                2401383885.000061,
                3401383885.000061,
                4401383885.000061
            ]
    '''
    removed = 0
    for ts in time_stamps:
        try:
            api.delete(ts)
            removed = removed + 1
            # 連続で送りすぎるとエラーになるので1秒待機
            time.sleep(1)
        except SlackApiError:
            print(traceback.format_exc())
    return removed


def main():
    # 発言内容と発言者の情報を削る（プライバシーの保護のため)
    messages = api.history()
    _messages = [m for m in map(filter_message, messages)]
    print(f'{len(_messages)}件のメッセージを取得しました')
    pprint(_messages)
    delete_target = select_delete_message(_messages)
    print(f'削除対象のメッセージが、{len(delete_target)}件ありました')
    pprint(delete_target)
    deleted_num = clean(delete_target)
    print(f'{len(delete_target)}件中{deleted_num}件のメッセージを削除しました')


if __name__ == "__main__":
    main()
