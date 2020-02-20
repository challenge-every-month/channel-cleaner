import unittest
import json
from unittest import mock
from requests import Response
from slack_api import SlackApi


class SlackApiTestCase(unittest.TestCase):
    def setUp(self):
	 self.responce_dict = {self.fail_responce, self.delete_responce, self.history_responce}
        self.fail_responce = {
            "ok": False,
            "error": "channel_not_found"
        }
        self.delete_responce = {
            "ok": True,
            "channel": "C024BE91L",
            "ts": "1401383885.000061"
        }
        self.history_responce = {
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
        with open('config.json') as config_file:
            self.api = SlackApi(json.load(config_file))
    
    def set_mock_response(testClassName, mock):
        # HTTPレスポンスのMockを作成する。
        res = Response()
        res.headers = {'Content-Type': 'application/json'}
        res.status_code = 200
        res._content = self.responce_dict[testClassName].encode('utf-8')
        mock.return_value = res
        

class DeleteTestCase(SlackApiTestCase):

    @mock.patch("requests.post")
    def test_success_delete_message(self, mock_post):
        '''削除APIを叩いて成功する'''
	set_mock_response('delete')
	api = SlackApi()
	result = api.delete()
	self .assertEqual
	
