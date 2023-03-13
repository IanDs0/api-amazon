FROM python:3.11.2

# ENV PYTHONUNBUFFERED 1

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

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]

#docker run --rm -d -p 80:80/tcp ianllhonrio/api_n_api:latest
#docker -t build ianllhonrio/api_n_api:latest