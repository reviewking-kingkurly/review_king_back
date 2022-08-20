import json
import re
import bcrypt

from django.views  import View
from django.http   import JsonResponse
from core.utils import Validation

from users.models  import User
from django.conf   import settings

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name             = data['user_name']
            email            = data['user_email']
            password         = data['user_password']
            
            REX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REX_PASSWORD = '^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,16}$'

            if User.objects.filter(email=email).exists():
                return JsonResponse({"Message": "ERROR_ACCOUNT_ALREADY_EXIST"}, status=400)
            if not re.match(REX_EMAIL, email):
                return JsonResponse({"Message": "INVALID_ACCOUNT"}, status=400)
            if not re.match(REX_PASSWORD, password):
                return JsonResponse({"Message": "INVALID_PASSWORD"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password
            )
            return JsonResponse({'Message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

class LogInView(View, Validation):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['user_email'])

            if not bcrypt.checkpw(data['user_password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)

            return JsonResponse({
                "message"      : "SUCCESS",     
                "access_token" : self.generate_jwt(user)
            }, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_ACCOUNT"}, status=404)