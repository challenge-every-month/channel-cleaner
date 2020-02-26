import json
import time
from datetime import  datetime, timedelta
from slack_api import SlackApi

with open('config.json') as config_file:
    api = SlackApi(json.load(config_file))

timelimit=datetime.now() + timedelta(hours=12)
history = api.history()

for m in history:
    delta = timelimit - parsedate_to_datetime(m['ts'])
    # メッセージの投稿時間が12時間前
    if delta>=12:
        api.delete(int(m['ts']))
        # 連続で送りすぎるとエラーになるので1秒待機
        time.sleep(1)
