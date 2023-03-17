FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

COPY SDK_Amazon/ /app
WORKDIR /app/paapi5-python-sdk-example
RUN python3 setup.py install

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY ./amazon ./amazon
COPY ./api_lojas ./api_lojas
COPY ./api_root ./api_root
COPY manage.py .
COPY .env .

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# RUN python3 manage.py createsuperuser --noinput --username admin --email admin@example.com

EXPOSE 8000

# docker network create minha-rede

# docker run -it -p 6379:6379 --name Redis --network minha-rede redis

# docker build -t django .
# docker run -it -p 8000:8000 --name Django --network minha-rede django bash


# CMD ["celery","-A","api_root","worker","-l","INFO"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# celery -A api_root worker -l INFO