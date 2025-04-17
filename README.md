# Test-task
1. Установить зависимостей:
python --version
python -m venv venv
.\venv\Scripts\activate (for Windows)
source venv/bin/activate (for Mac/Linux)
pip install django/pillow/
2. Настройка бд:
python manage.py migrate
3. Создание суперюзера:
python manage.py createsuperuser
4. Запуск сервера:
python manage.py runserver
5. Для запуска теста:
python manage.py test
6. Для доступа к админке:
http://127.0.0.1:8000/admin/