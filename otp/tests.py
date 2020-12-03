import datetime
import time

from django.test import Client

from django.test import TestCase


# Create your tests here.

class OTPTestCase(TestCase):
    def setUp(self) -> None:
        print('now:' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def test_get(self) -> None:
        c = Client()
        for i in range(20):
            response = c.get('/api/otp/')
            data = response.data
            time.sleep(1)
            print(data)
            resp = c.post('/api/otp/',data={'TOTP':data['TOTP'],'HOTP':data['HOTP'],'count':data['count']})
            print(resp.data)



