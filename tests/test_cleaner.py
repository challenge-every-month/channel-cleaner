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


class testGetAllMessage(unittest.TestCase):

    @mock.patch("slack_api.SlackApi.history")
    @mock.patch("slack_api.SlackApi.replies")
    def test_メッセージにスレッドがある時スレッドを取得してくる(self, mock_replies, mock_history):
        mock_history.return_value = [
            {'blocks': [{'block_id': '0H1X',
                                     'elements': [{'elements': [{'text': 'hoge', 'type': 'text'}],
                                                   'type': 'rich_text_section'}],
                                     'type': 'rich_text'}],
             'client_msg_id': '78ca7405-98c3-4555-9130-4c4c773f1e1d',
             'last_read': '1583333641.004400',
             'latest_reply': '1583333641.004400',
             'reply_count': 1,
             'reply_users': ['UUKH261KQ'],
             'reply_users_count': 1,
             'subscribed': True,
             'team': 'TUK6UHQMV',
             'text': 'hoge',
             'thread_ts': '1583333634.004300',
             'ts': '1583333634.004300',
             'type': 'message',
             'user': 'UUKH261KQ'}]
        mock_replies.return_value = [
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "three for the land",
                "thread_ts": "1583333634.004300",
                "parent_user_id": "U061F7AUR",
                "ts": "1483125339.020269"
            }
        ]
        expect = [
            {'blocks': [{'block_id': '0H1X',
                         'elements': [{'elements': [{'text': 'hoge', 'type': 'text'}],
                                       'type': 'rich_text_section'}],
                         'type': 'rich_text'}],
             'client_msg_id': '78ca7405-98c3-4555-9130-4c4c773f1e1d',
             'last_read': '1583333641.004400',
             'latest_reply': '1583333641.004400',
             'reply_count': 1,
             'reply_users': ['UUKH261KQ'],
             'reply_users_count': 1,
             'subscribed': True,
             'team': 'TUK6UHQMV',
             'text': 'hoge',
             'thread_ts': '1583333634.004300',
             'ts': '1583333634.004300',
                   'type': 'message',
                   'user': 'UUKH261KQ'},
            {
                "type": "message",
                "user": "U061F7AUR",
                "text": "three for the land",
                "thread_ts": "1583333634.004300",
                "parent_user_id": "U061F7AUR",
                "ts": "1483125339.020269"
            }]
        actual = cleaner.get_all_message()
        self.assertEqual(expect, actual)
