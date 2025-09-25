from django.contrib.auth.backends import ModelBackend, BaseBackend

from django.contrib.auth import get_user_model




class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model()
        User = get_user_model()

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
                else:
                    return None

            except User.DoesNotExist:
                return  None
            


            

def service():
    ACCEPTED_MAIL_FREE_SERVICE = ["@ucalgary.ca"]
    # We need to get user's email, and we can use string concetation to find the email, or endswith "@Ucalgary.ca"
    # if EmailBackEnd(email).endswith("@ucalgary.ca"):
    #     pass

def verification():
    # We'll send a verifcation code, and use randomized letter, numbers, and symbols to create a code. We'll check if the user's verification code matches in our database. #Send via: Google, Yahoo, Outlook, etc.
    pass


