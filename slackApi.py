import requests
from typing import Dict, List
import SlackApiError


class slackApi():

    def __init__(self, api_tokens: Dict[str, str]):
        self.token = api_tokens.get('token')
        self.channel_id = api_tokens.get('channel_id')

        """
        tokenとchannelのIDを受け取る

        Args:
            api_tokens: tokenとchannel_idを受け取る辞書
            channel_idは、省略可能
            {
                token:[your token],
                channel_id:[channel_id]
            }
        """

    def say(self, message: str, channel_id: str=""):
        """
        slackへ発言を投稿する
        channel_idを省略した場合、__init__で渡した channel_idを利用する

        Args:
            message: 投稿するメッセージを入力する
            channel_id: 投稿するチャンネルを指定するばあいはここにchannel_idを渡す
        """
        pass

    def delete(self, time_stamp: int, channel_id: str=""):
        delete_url = "https://slack.com/api/chat.delete"
        delete_params = {'token': self.token,
                         'channel': channel_id if len(channel_id) > 0 else self.channel_id
                         }

        """
        特定のチャンネルの発言を削除する
        channel_idを省略した場合、__init__で渡した channel_idを利用する

        Args:
            time_stamp : 削除したいメッセージのタイムスタンプ(ex:1405894322.002768)
            channel_id : 削除する発言のあるチャンネルを指定するばあいはここにchannel_idを渡す
        """

    def history(self, channel_id: str="", limit: int=1000) -> List[Dict[str, str]]:
        hist_url = "https://slack.com/api/channels.history"
        hist_params = {'token': self.token,
                       'channel': channel_id if len(channel_id) > 0 else self.channel_id,
                       'count': limit,
                       }
        self.history_data = self._request_api(hist_url, hist_params, "GET")
        if self.history_data['ok']:
            return self.history_data['messages']
        else:
            raise SlackApiError(self.history_data['error'])

        """
        特定のチャンネルの発言を取得する

        Args:
            channel_id: 投稿するチャンネルを指定するばあいはここにchannel_idを渡す
            limit: 取得上限を設定する。
        """

    def _request_api(self, url: str, data: Dict, method: str="GET"):
        header = {'Content-Type', 'application/x-www-form-urlencoded'}
        if method.lower() == "get":
            res = requests.get(url, header=header, data=data)
        elif method.lower() == "post":
            res = requests.post(url, header=header, data=data)
        res.raise_for_status()
        return res.json()
