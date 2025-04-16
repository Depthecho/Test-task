from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class AuthService:
    @staticmethod
    def register_user(request, form_data=None):
        if request.method == 'POST':
            form = UserCreationForm(form_data or request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Аккаунт успешно создан!')
                return True
            messages.error(request, 'Ошибка при регистрации!')
        return False

    @staticmethod
    def login_user(request, username=None, password=None):
        if request.method == 'POST':
            username = username or request.POST.get('username')
            password = password or request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return True
            messages.error(request, 'Неверные данные для входа!')
        return False

    @staticmethod
    def logout_user(request):
        logout(request)
        return True