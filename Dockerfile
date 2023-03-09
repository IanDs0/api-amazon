FROM python:3.11.2

COPY SDK_Amazon/ /app
WORKDIR /app/paapi5-python-sdk-example
RUN python3 setup.py install

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY ./src ./src
COPY main.py .
COPY .env .

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]#uvicorn main:app --host 0.0.0.0 --port 80

#docker run --rm -d -p 80:80/tcp ianllhonrio/api_n_api:latest
#docker -t build ianllhonrio/api_n_api:latest