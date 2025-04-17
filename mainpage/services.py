from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm


class AuthService:
    # Сервис для аутентификации пользователей: регистрация, вход, выход.

    @staticmethod
    def register_user(request):
        # Регистрация пользователя и вход в систему.
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Аккаунт успешно создан!')
                return True, form
            messages.error(request, 'Ошибка при регистрации!')
            return False, form
        else:
            form = CustomUserCreationForm()
            return None, form

    @staticmethod
    def login_user(request):
        # Авторизация пользователя.
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return True
            messages.error(request, 'Неверные данные для входа!')
        return False

    @staticmethod
    def logout_user(request):
        # Выход пользователя из системы.
        logout(request)
        return True
