from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Ensure username exists (Google email → username)
        if not user.username:
            user.username = user_username(user)

        # Default fields for Google users
        user.role = "Team Member"
        user.department = ""

        return user
