from django.conf import settings
from ws4py.client.geventclient import WebSocketClient


class CustomWs(WebSocketClient):

    def closed(self, code, reason=None):
        try:
            self.close()
            self.connect()
        except Exception as e:
            print("PushServer error")
            print(e)

    def received_message(self, message):
        print(message)


ws = CustomWs(settings.PUSH_SERVER + 'server/Auth/', heartbeat_freq=5)
# ws = CustomWs('ws://127.0.0.1:8891/' + 'server/Auth/', heartbeat_freq=5)
ws.connect()
