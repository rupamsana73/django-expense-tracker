from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
def auth_view(request):

    # SIGNUP
    if request.method == "POST" and 'signup' in request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('auth')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('auth')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('/dashboard/')

    # LOGIN
    if request.method == "POST" and 'login' in request.POST:
        email = request.POST['email']
        password = request.POST['password']

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('auth')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid password")
            return redirect('auth')

    return render(request, 'accounts/auth.html')


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.profile.image = request.FILES.get('image')
        request.user.profile.save()
        return redirect('dashboard')

    return render(request, 'accounts/profile.html')
