# Используем базовый образ с Python
FROM python

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта из локального контекста сборки в контейнер
COPY /src/ /app/
COPY /text_files/ /app/text_files/

# Копируем файл requirements.txt
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем ваш бот
CMD ["python", "main.py"]
