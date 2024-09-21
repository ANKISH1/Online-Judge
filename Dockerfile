FROM python:3.9
RUN apt-get update && apt-get install -y g++
RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY . /app
RUN pip install --no-cache django
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=OnlineJudge.settings
ENV PYTHONUNBUFFERED=1
CMD ["python", "manage.py", "runserver", "0.0.0.0aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/z2k5k0n8:8000"]