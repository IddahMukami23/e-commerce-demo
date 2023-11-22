from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from userAuth.forms import UserRegisterForm
from userAuth.models import User
from django.conf import settings

# User = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, account created successfully")
            new_user = authenticate(username=form.cleaned_data.get('email'),
                                    password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'userAuth/sign-in.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect('home')
            else:
                messages.warning(request, "Incorrect password. Please try again.")

        except User.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist")
            return render(request, 'userAuth/login.html')

    return render(request, 'userAuth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You've logged out successfully")
    return redirect('login')
