import jwt
import datetime
from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.conf import settings
from auth_app.models import User

def is_admin(view_func):
    @wraps(view_func)
    def wrapped_view(request,user_id=None ,clear=False , *args, **kwargs):
        jwt_token = request.headers.get('Authorization', '').split(' ')[1]
        try:
            decoded_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": True})
            jwt_user_id = decoded_token['user_id']
            user = User.objects.get(id=jwt_user_id)
            
            if not user.is_staff:
                print(f"[{datetime.datetime.now()}]error: The user {jwt_user_id} has insufficient rights ")
                return JsonResponse({'message': 'Not enough rights'}, status=status.HTTP_403_FORBIDDEN)

            if clear:
                token_obj = RefreshToken.for_user(user_id)
                token_obj.blacklist()

            
            return view_func(request, user_id, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            print(f"[{datetime.datetime.now()}]error: JWT user {jwt_user_id} expired")
            return JsonResponse({'message': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            print(f"[{datetime.datetime.now()}]error: Invalid token")
            return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            print(f"[{datetime.datetime.now()}]error: User not found")
            return JsonResponse({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: {str(e)}")
            return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return wrapped_view
