FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir telethon pillow

CMD ["python", "avatar_updater.py"]
