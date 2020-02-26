import unittest
from datetime import datetime, timedelta
from unittest import mock


import cleaner


class cleanerTestCase(unittest.TestCase):
    now_time = datetime.strptime('2020/02/26 11:02:27', '%Y/%m/%d %H:%M:%S')
    timelimit = now_time + timedelta(hours=12)

    @mock.patch("cleaner.slack_api.SlackApi.history")
    @mock.patch("slack_api.SlackApi.delete")
    def 投稿時間が12時間前のメッセージだけを削除APIに投げる(self, mock_history, mock_delete):

        mock_history.return_value = [
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "I find you punny and would like to smell your nose letter",
                "ts": self.time_stamp.timestamp()
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "What, you want to smell my shoes better?",
                "ts": self.now_time.timestamp()
            },
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system",
                "ts": self.now_time.timestamp()
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "that they cannot foresee",
                "ts": self.now_time.timestamp()
            }
        ]
        cleaner.clean()
        mock_delete.assert_called_with(self.time_stamp.timestamp())