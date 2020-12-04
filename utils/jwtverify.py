import requests
from functools import wraps
from django.conf import settings
from .api_response import JsonResponse

from django.contrib.auth.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username
    }


# Production Server
def JWTVerify(func):
    @wraps(func)
    def handler(self, *args, **kwargs):
        Token = 'Authorization'
        if Token not in self.request.headers.keys():
            return JsonResponse(data={}, code='-1', msg='token needed')
        token = self.request.headers[Token]
        try:
            res = requests.post(settings.AUTH_SERVER + 'jwt-verify', data={'token': token})
        except Exception as e:
            return JsonResponse(data={}, code="-2", msg='auth server error')
        rcv = res.json()
        if res.status_code == 400:
            if rcv['non_field_errors'][0] == 'Signature has expired.':
                return JsonResponse(data={}, code="-2", msg='token expired')
            else:
                return JsonResponse(data={}, code="-1", msg='token error')
        if res.status_code == 200:
            self.request.user = rcv['user']
            return func(self, *args, **kwargs)

    return handler
