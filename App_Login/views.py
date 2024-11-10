from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Forms and Models
from App_Login.models import Profile
from App_Login.forms import ProfileForm, SignUpForm

# Messages package
from django.contrib import messages 

from App_Login.models import User

# Create your views here.
def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully :D')
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/sign_up.html', context={'form':form})

def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Bazar:home'))
    
    return render(request, 'App_Login/login.html', context={'form':form})

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)

    form = ProfileForm(instance = profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, "Profile updated successfully :D")
            form = ProfileForm(instance=profile)
    
    return render(request, 'App_Login/change_profile.html', context={'form':form})

@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password updated successfully :D')
            return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/change_password.html', context={'form':form})
@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'Logged out')
    return HttpResponseRedirect(reverse('App_Login:login'))

@login_required
def all_users(request):
    users = User.objects.all()
    return render(request, 'App_Login/all_users.html', context={'users':users})