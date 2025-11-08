from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


# 🟩 REGISTER VIEW
def register_view(request):
    """Handles new user registration."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created successfully! You can now log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# 🟦 LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirect based on role
            if user.role == "HR":
                return redirect("dashboard:hr_dashboard")

            elif user.role == "Manager":
                return redirect("dashboard:dashboard")

            elif user.role == "Team Member":
                return redirect("dashboard:dashboard")

            # default fallback
            return redirect("dashboard:dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# 🟥 LOGOUT VIEW
@login_required
def logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('accounts:login')
