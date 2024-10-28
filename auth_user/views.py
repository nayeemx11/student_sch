from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'index.html')


from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import redirect, render
from schoolarship.models import Student
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new CustomUser instance
            if user.position_status == "Student":  # Check if the user is a student
                Student.objects.create(user=user)  # Adjust ID generation logic
            auth_login(request, user)  # Automatically log in the new user
            messages.success(request, "Account created successfully! Welcome!")
            return redirect("index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Using the built-in form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('index')  # Redirect to your desired page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    
    else:
        form = AuthenticationForm()  # Display empty form

    return render(request, 'login.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login after logging out
