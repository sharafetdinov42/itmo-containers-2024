FROM python:3.12-slim

# Устанавливаем необходимые пакеты для компиляции и зависимость libpq-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    libxml2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения и без установки dev-зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

# Копируем весь код
COPY . .

# Открываем порт для Streamlit
EXPOSE 27369

# Команда для запуска Streamlit-приложения
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=27369"]
