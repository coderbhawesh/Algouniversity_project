FROM python:3.9
RUN apt-get update && apt-get install -y clang
WORKDIR /app
COPY . /app


RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED=1

CMD ["python","manage.py","runserver","0.0.0.0:8000"]