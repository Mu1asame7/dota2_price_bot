# Базовый образ
FROM python:3.12-slim

# Устанавливаем системные зависимости (ЭТО НУЖНО ДЕЛАТЬ ПЕРВЫМ, до создания пользователя)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Создаем непривилегированного пользователя (ТЕПЕРЬ ЭТО БЕЗОПАСНО)
RUN adduser --disabled-password --gecos "" appuser

# Переключаемся на обычного пользователя
USER appuser

# Команда запуска
CMD ["gunicorn", "dota2_bot_project.wsgi:application", "--bind", "0.0.0.0:10000"]