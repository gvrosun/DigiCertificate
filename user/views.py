from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'user/index.html')


def login(request):
    return render(request, 'user/login.html')


def register(request):
    return render(request, 'user/register.html')


def forgot_password(request):
    return render(request, 'user/forgot-password.html')


def logout(request):
    return redirect(index)


# Handling Exceptions
def handle_404_error(request, exception):
    return render(request, 'user/404.html')
