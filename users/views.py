from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect(reverse('users:login'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('sales:index'))  # Redirect to the index function of the 'sales' app if logged in
        else:
            messages.error(request, "Invalid username or password")
            return redirect(reverse('users:login'))  # Redirect back to login on failure
    return render(request, 'users/login.html')  # Render login form for GET request


# Logout view
def logout_view(request):
    logout(request)
    return redirect(reverse('users:login'))  # Redirect to the login page after logging out


@login_required
def perfil(request):
    # Move imports here to avoid circular imports
    from .forms import ProfileForm
    from .models import Profile
    
    user = request.user
    # Ensure the user has a profile. Create one if it doesn't exist.
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'sales/perfil.html', {'form': form, 'user': user})