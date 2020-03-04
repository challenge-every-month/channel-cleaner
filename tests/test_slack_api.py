import unittest
import json
import os
import os.path
from unittest import mock
from requests import Response
from slack_api import SlackApi, exception
import types


class SlackApiTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.time_stamp = "1401383885.000061"
        with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
            config_json = json.load(config_file)
            self.channel_id = config_json['channel_id']
            self.token = config_json['token']
            self.api = SlackApi(self.token, self.channel_id)

        self.params = {'token': self.token,
                       'channel': self.channel_id,
                       'count': 1000,
                       }
        self.fail_response = {
            "ok": False,
            "error": "channel_not_found"
        }
        self.delete_response = {
            "ok": True,
            "channel": self.channel_id,
            "ts": self.time_stamp
        }
        self.history_response = {
            "ok": True,
            "messages": [
                {
                    "type": "message",
                    "user": "U012AB3CDE",
                    "text": "I find you punny and would like to smell your nose letter",
                    "ts": self.time_stamp
                },
                {
                    "type": "message",
                    "user": "U061F7AUR",
                    "text": "What, you want to smell my shoes better?",
                    "ts": self.time_stamp
                }
            ],
            "has_more": True,
            "pin_count": 0,
            "response_metadata": {
                "next_cursor": "bmV4dF90czoxNTEyMDg1ODYxMDAwNTQz"
            }
        }
        self.history_response2 = {
            "ok": True,
            "messages": [
                {
                    "type": "message",
                    "user": "U012AB3CDE",
                    "text": "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system",
                    "ts": self.time_stamp
                },
                {
                    "type": "message",
                    "user": "U061F7AUR",
                    "text": "that they cannot foresee",
                    "ts": self.time_stamp
                }
            ],
            "has_more": False,
            "pin_count": 0,
            "response_metadata": {
                "next_cursor": ""
            }
        }

        def set_history_response():
            yield self.history_response
            yield self.history_response2
        history_responses = set_history_response()

        self.response_dict = {"fail": self.fail_response, "delete": self.delete_response, "history": history_responses}

    def set_mock_response(self, testClassName, mock):
        def set_http_responce(url, data={}, params={}, headers={}):
            # HTTPレスポンスのMockを作成する。
            res = Response()
            res.headers = {'Content-Type': 'application/json'}
            res.status_code = 200
            res_dict = self.response_dict[testClassName]
            content = res_dict if not isinstance(res_dict, types.GeneratorType) else next(res_dict)
            res._content = json.dumps(content).encode('utf-8')
            return res
        mock.side_effect = set_http_responce


class DeleteTestCase(SlackApiTestCase):
    testClassName = "delete"

    @mock.patch("requests.post")
    def test_SlackAPIを呼び出せる(self, mock_post):
        self.set_mock_response(self.testClassName, mock_post)
        result = self.api.delete(self.time_stamp)
        self.assertEqual(result, self.delete_response)

    @mock.patch("requests.post")
    def test_指定したチャンネルIDでAPIを呼び出せる(self, mock_post):
        self.delete_response['channel'] = 'A024BE91L'
        self.set_mock_response(self.testClassName, mock_post)
        result = self.api.delete(self.time_stamp)
        self.assertEqual(result, self.delete_response)

    @mock.patch("requests.post")
    def test_SlackAPIの実行に失敗した時SlackAPIErrorが返る(self, mock_post):
        self.set_mock_response("fail", mock_post)
        with self.assertRaises(exception.SlackApiError):
            self.api.delete(self.time_stamp)


class HistoryTestCase(SlackApiTestCase):
    testClassName = "history"
    url = "conversations.history"

    @mock.patch("requests.get")
    def test_SlackAPIを呼び出せる(self, mock_post):
        expect_responce = [
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "I find you punny and would like to smell your nose letter",
                "ts": self.time_stamp
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "What, you want to smell my shoes better?",
                "ts": self.time_stamp
            },
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system",
                "ts": self.time_stamp
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "that they cannot foresee",
                "ts": self.time_stamp
            }
        ]
        self.set_mock_response(self.testClassName, mock_post)
        result = self.api.history()
        self.assertEqual(result, expect_responce)

    @mock.patch("slack_api.SlackApi._request_api")
    def test_指定したチャンネルIDでAPIを呼び出せる(self, mock_api):
        channel_id = 'A024BE91L'
        self.history_response['channel'] = channel_id
        self.params['channel'] = channel_id
        mock_api.return_value = self.history_response2
        self.api.history(channel_id=channel_id)
        mock_api.assert_called_with(self.url, self.params, "GET")

    @mock.patch("slack_api.SlackApi._request_api")
    def test_指定した上限数でAPIを呼び出せる(self, mock_api):
        limit = 999
        self.params['count'] = limit
        mock_api.return_value = self.history_response2
        self.api.history(limit)
        mock_api.assert_called_with(self.url, self.params, "GET")

    @mock.patch("requests.get")
    def test_SlackAPIの実行に失敗した時SlackAPIErrorが返る(self, mock_post):
        self.set_mock_response("fail", mock_post)
        with self.assertRaises(exception.SlackApiError):
            self.api.history()
