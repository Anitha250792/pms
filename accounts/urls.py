from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from allauth.account.views import LoginView, SignupView

app_name = "accounts"

def instant_logout(request):
    logout(request)
    return redirect("accounts:account_login")

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="account/login.html"),
        name="account_login"
    ),

    path(
        "register/",
        SignupView.as_view(template_name="account/signup.html"),
        name="account_signup"
    ),

    path(
        "logout/",
        instant_logout,
        name="account_logout"
    ),
]
