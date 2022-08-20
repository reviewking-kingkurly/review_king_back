import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.http import JsonResponse

from users.models import User

class Validation:
    def generate_jwt(self, user):
        payload      = {'user_id': user.id, 'exp': datetime.now() +timedelta(hours=2)}
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return access_token

def login_decorator(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user         = User.objects.get(id = payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError: 
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message' : 'EXPIRED_TOKEN'}, status=401)

        return func(self,request,*args,**kwargs)
    return wrapper