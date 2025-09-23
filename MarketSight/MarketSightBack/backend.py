from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class EmailBackEnd(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model()
        username = request.POST.get("username") # This will grab the username from any views.py when authenticate is used (This is just recreating the authenticate function, but adding email.)
        password = request.POST.get('password')

        email = kwargs.get('email')
        if email is None:
            return None # This is my version of ensuring that email is required for login
        else:
            try:
                user = User.objects.get(email=email)
                # This will ensure that our password is secure "password123" would
                # turn into a convoluted mess
                if user.check_password(password): 
                    return user

            except User.DoesNotExist:
                return  None