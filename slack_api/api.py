import requests
import os
from typing import Dict, List
from .exception import SlackApiError
from urllib.parse import urljoin


class SlackApi():

    def __init__(self, token, channel_id=''):
        '''
        tokenとchannelのIDを受け取る

        Args:
            api_tokens: tokenとchannel_idを受け取る辞書
            channel_idは、省略可能
            {
                token:[your token],
                channel_id:[channel_id]
            }
        '''
        self.token = token
        self.channel_id = channel_id

    def say(self, message: str, channel_id: str = ''):
        '''
        slackへ発言を投稿する
        channel_idを省略した場合、__init__で渡した channel_idを利用する

        Args:
            message: 投稿するメッセージを入力する
            channel_id: 投稿するチャンネルを指定するばあいはここにchannel_idを渡す
        '''
        end_point = 'chat.postMessage'
        params = {'token': self.token,
                  'channel': channel_id if len(channel_id) > 0 else self.channel_id
                  }

        result = self._request_api(end_point, params, 'POST')

        return result

    def delete(self, time_stamp: str, channel_id: str = ''):
        '''
        特定のチャンネルの発言を削除する
        channel_idを省略した場合、__init__で渡した channel_idを利用する

        Args:
            time_stamp : 削除したいメッセージのタイムスタンプ(ex:1405894322.002768)
            channel_id : 削除する発言のあるチャンネルを指定するばあいはここにchannel_idを渡す
        '''

        end_point = 'chat.delete'
        params = {'token': self.token,
                  'channel': channel_id if len(channel_id) > 0 else self.channel_id,
                  'ts': time_stamp
                  }

        result = self._request_api(end_point, params, 'POST')

        return result

    def history(self, limit: int = 1000, channel_id: str = '') -> List[Dict[str, str]]:
        '''
        特定のチャンネルの発言を取得する

        Args:
            channel_id: 投稿するチャンネルを指定するばあいはここにchannel_idを渡す
            limit: 取得上限を設定する。
        '''

        end_point = 'conversations.history'
        params = {'token': self.token,
                  'channel': channel_id if len(channel_id) > 0 else self.channel_id,
                  'count': limit,
                  }
        res  = self._request_api(end_point, params, 'GET')
        messages = res['messages']
        while res['has_more']:
            params['cursor'] = res['response_metadata']['next_cursor']
            res  = self._request_api(end_point, params, 'GET')
            messages.extend([message for message in res['messages']])
        return messages

    def _request_api(self, end_point: str, data: Dict, method: str = 'GET'):
        url = urljoin('https://slack.com/api/', end_point)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        if method.lower() == 'get':
            res = requests.get(url, headers=header, params=data)
        elif method.lower() == 'post':
            res = requests.post(url, headers=header, data=data)

        res.raise_for_status()
        res_json = res.json()

        # Slack APIの実行に失敗した時、例外を返す
        if not res_json.get('ok'):
            raise SlackApiError(res_json.get('error'))

        return res_json
