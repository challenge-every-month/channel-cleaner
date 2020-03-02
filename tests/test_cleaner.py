import unittest
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import call


import cleaner


class cleanerTestCase(unittest.TestCase):
    now_time = datetime.now()
    time_limit_exceeded = now_time - timedelta(hours=12)
    time_limit_exceeded_2 = now_time - timedelta(hours=13)
    with_in_time_limit = now_time - timedelta(hours=11)

    @mock.patch("slack_api.SlackApi.history")
    @mock.patch("slack_api.SlackApi.delete")
    def test_投稿時間が12時間前のメッセージだけを削除APIに投げる(self, mock_delete, mock_history):

        mock_history.return_value = [
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "I find you punny and would like to smell your nose letter",
                "ts": str(self.time_limit_exceeded.timestamp())
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "What, you want to smell my shoes better?",
                "ts": str(self.now_time.timestamp())
            },
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system",
                "ts": str(self.now_time.timestamp())
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "that they cannot foresee",
                "ts": str(self.now_time.timestamp())
            }
        ]
        cleaner.main()
        mock_delete.assert_called_once_with(str(self.time_limit_exceeded.timestamp()))

    @mock.patch("slack_api.SlackApi.history")
    @mock.patch("slack_api.SlackApi.delete")
    def test_投稿時間が12時間以前の複数のメッセージを削除APIに投げる(self, mock_delete, mock_history):

        mock_history.return_value = [
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "I find you punny and would like to smell your nose letter",
                "ts": self.time_limit_exceeded.timestamp()
            },
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "What, you want to smell my shoes better?",
                "ts": self.time_limit_exceeded_2.timestamp()
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
        cleaner.main()
        mock_delete.assert_any_call(self.time_limit_exceeded.timestamp())
        mock_delete.assert_any_call(self.time_limit_exceeded_2.timestamp())

    @mock.patch("slack_api.SlackApi.history")
    @mock.patch("slack_api.SlackApi.delete")
    def test_投稿時間が11時間前のメッセージは削除APIに投げない(self, mock_delete, mock_history):

        mock_history.return_value = [
            {
                "type": "message",
                "user": "U012AB3CDE",
                "text": "I find you punny and would like to smell your nose letter",
                "ts": self. with_in_time_limit.timestamp()
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
        cleaner.main()
        mock_delete.assert_not_called()