import unittest
import json
import os
import os.path
from unittest import mock
from requests import Response
from slack_api import SlackApi


class SlackApiTestCase(unittest.TestCase):
    def setUp(self):
        self.fail_response = {
            "ok": False,
            "error": "channel_not_found"
        }
        self.delete_response = {
            "ok": True,
            "channel": "C024BE91L",
            "ts": "1401383885.000061"
        }
        self.history_response = {
            "ok": True,
            "messages": [
                {
                    "type": "message",
                    "user": "U012AB3CDE",
                    "text": "I find you punny and would like to smell your nose letter",
                    "ts": "1512085950.000216"
                },
                {
                    "type": "message",
                    "user": "U061F7AUR",
                    "text": "What, you want to smell my shoes better?",
                    "ts": "1512104434.000490"
                }
            ],
            "has_more": True,
            "pin_count": 0,
            "response_metadata": {
                "next_cursor": "bmV4dF90czoxNTEyMDg1ODYxMDAwNTQz"
            }
        }
        self.response_dict = {"fail": self.fail_response, "delete": self.delete_response, "histor":self.history_response}
        with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
            self.api = SlackApi(json.load(config_file))

    def set_mock_response(self, testClassName, mock):
        # HTTPレスポンスのMockを作成する。
        res = Response()
        res.headers = {'Content-Type': 'application/json'}
        res.status_code = 200
        res._content = json.dumps(self.response_dict[testClassName]).encode('utf-8')
        mock.return_value = res


class DeleteTestCase(SlackApiTestCase):

    @mock.patch("requests.post")
    def test_success_delete_message(self, mock_post):
        '''削除APIを叩いて成功する'''
        self.set_mock_response('delete', mock_post)
        result = self.api.delete('1401383885.000061')
        self.assertEqual(result, self.delete_response)


    @mock.patch("requests.post")
    def test_success_delete_message_specified_channel(self, mock_post):
        '''チャンネルIDを指定して削除APIを叩いて成功する'''
        channel_id = 'A024BE91L'
        self.delete_response['channel']
        self.set_mock_response('delete', mock_post)
        result = self.api.delete('1401383885.000061', channel_id)
        self.assertEqual(result, self.delete_response)


class HistoryTestCase(SlackApiTestCase):

    @mock.patch("requests.post")
    def test_success_delete_message(self, mock_post):
        '''削除APIを叩いて成功する'''
        self.set_mock_response('delete', mock_post)
        result = self.api.delete('1401383885.000061')
        self.assertEqual(result, self.delete_response)


    @mock.patch("requests.post")
    def test_success_delete_message_specified_channel(self, mock_post):
        '''チャンネルIDを指定して削除APIを叩いて成功する'''
        channel_id = 'A024BE91L'
        self.delete_response['channel']
        self.set_mock_response('delete', mock_post)
        result = self.api.delete('1401383885.000061', channel_id)
        self.assertEqual(result, self.delete_response)
