FROM python:3.11.9-slim

WORKDIR /app

# Оновлюємо систему та встановлюємо необхідні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо та встановлюємо Python залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код
COPY . .

# Запускаємо бота
CMD ["python", "main.py"]
