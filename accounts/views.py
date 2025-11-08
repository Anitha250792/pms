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
    """Handles user login with namespace-safe redirection."""
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"🎉 Welcome, {user.username}!")

            # ✅ If ?next=/dashboard/, redirect there first
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            # ✅ Safe redirect to Dashboard (works even if namespace changes)
            try:
                return redirect(reverse('dashboard:dashboard'))
            except NoReverseMatch:
                # Fallback in case namespace not loaded yet
                return redirect('/dashboard/')

        else:
            messages.error(request, "Invalid username or password.")
    elif request.method == 'POST':
        messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'accounts/login.html', {'form': form})


# 🟥 LOGOUT VIEW
@login_required
def logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('accounts:login')
