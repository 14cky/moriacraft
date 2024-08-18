from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.utils import translation
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import SignUpForm

@login_required(login_url='login')
def kidsignup(request):
    return render(request, 'kidsignup.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def lessons(request):
    return render(request, 'lessons.html')

@login_required(login_url='login')
def premium(request):
    return render(request, 'premium.html')

@login_required(login_url='login')
def notes(request):
    return render(request, 'notes.html')

@login_required(login_url='login')
def note1(request):
    return render(request, 'note1.html')

@login_required(login_url='login')
def profileview(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard or another page after saving
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'email': user.email,
            'password': ''  # Don't pre-fill password for security reasons
        })

    return render(request, 'profile.html', {'form': form})

def home(request):
    if 'language' in request.POST:
        lang_code = request.POST['language']
        translation.activate(lang_code)
        request.session['django_language'] = lang_code
        return redirect('login')
    return render(request, 'index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)  # Correctly log the user in after signup
            messages.success(request, _('Account created successfully!'))
            return redirect('dashboard')  # Redirect to the home page or dashboard after signup
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def ulogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data.get('email_or_phone')
            password = form.cleaned_data.get('password')

            # Determine if the input is an email or a username
            if '@' in email_or_phone:
                # Extract the username part from the email
                username = email_or_phone.split('@')[0]
            else:
                # Assume it's a username or phone
                username = email_or_phone

            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)

            # Handle the case where the username generated from the email is not unique
            if user is None:
                try:
                    user = User.objects.get(email=email_or_phone)
                    user = authenticate(request, username=user.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                request.session.set_expiry(30*24*60*60)
                return redirect('dashboard')
            else:
                messages.error(request, _('Invalid login credentials.'))

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def game(request):
    return render(request, 'game.html')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, _('Your profile has been updated!'))
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'profile.html', context)