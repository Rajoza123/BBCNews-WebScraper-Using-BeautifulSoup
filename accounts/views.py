from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email or username already exists before creating a new user
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose another.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email or log in.')
            return render(request, 'signup.html')

        try:
            # Attempt to create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        except IntegrityError:
            # Handle database integrity issues like duplicate fields
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']  # Use 'username' if you're using usernames for login
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
