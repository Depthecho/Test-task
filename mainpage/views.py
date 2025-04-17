from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .services import AuthService


def register_view(request):
    auth_service = AuthService()
    result, form = auth_service.register_user(request)

    if result is True:
        return redirect('ad_list')

    return render(request, 'mainpage/register.html', {'form': form})


def login_view(request):
    auth_service = AuthService()
    result = auth_service.login_user(request)

    if result is True:
        return redirect('ad_list')

    return render(request, 'mainpage/login.html')


@login_required
def logout_view(request):
    auth_service = AuthService()
    auth_service.logout_user(request)
    return redirect('ad_list')
