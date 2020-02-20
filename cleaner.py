import requests
import json
import time


with open("config.json") as config_file:
    config = json.load(config_file)
token = config['token']
channel = config.get['channel_id']




for m in data["messages"]:
    delete_params['ts'] = m["ts"]
    enc_params = urllib.urlencode(delete_params)

    req = urllib2.Request(delete_url)
    req.add_header()
    req.add_data(enc_params)

    res = urllib2.urlopen(req)

    body = res.read()
    print(body)
    # 連続で送りすぎるとエラーになるので1秒待機
    time.sleep(1)
