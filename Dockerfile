FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

COPY SDK_Amazon/ /app
WORKDIR /app/paapi5-python-sdk-example
RUN python3 setup.py install

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY . .

RUN rm -r SDK_Amazon

# RUN python3 manage.py makemigrations

EXPOSE 8000