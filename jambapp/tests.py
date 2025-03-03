from django.test import TestCase


class TestSK(TestCase):
    def setUp(self):
        self.email = 'user@mail'
        self.tid = 1759227585

    def test_check_transaction_status(self):
        res = self.client.get(f'/cts/{self.tid}/')
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.content.decode(), 'check success')
