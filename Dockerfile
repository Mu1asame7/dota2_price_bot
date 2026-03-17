# Базовый образ — "чистый лист" с Python [citation:2]
FROM python:3.11-slim

# Отключаем запись .pyc файлов и буферизацию вывода (чтобы логи сразу появлялись) [citation:2]
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем рабочую папку внутри контейнера [citation:2]
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их [citation:2]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь наш проект внутрь контейнера [citation:2]
COPY . .

# Создаем непривилегированного пользователя для безопасности [citation:2]
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Команда по умолчанию (она будет переопределена в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]