from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.rest import ApiException
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define as credenciais de acesso da AWS
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
host = os.getenv('HOST')
region = os.getenv('REGION')

def Search(Keywords, SearchIndex, ItemCount):
    # Cria uma instância do objeto DefaultApi
    api_instance = DefaultApi(access_key, secret_key, host, region)


    # Define os parâmetros de pesquisa
    search_request = {
        'Keywords': Keywords, #'livros de programação',
        'SearchIndex': SearchIndex, #'Books',
        'ItemCount': ItemCount, #10
    }

    try:
        # Realiza a pesquisa de itens
        response = api_instance.search_items(search_request)
        print(response)
        return response
    except ApiException as e:
        print(f'Error calling PAAPI5 SearchItems operation: {e}')
        return "Error"


class Buscar(BaseModel):
    Keywords: str
    SearchIndex: str
    ItemCount: int



def Json (retorno):
    retornando = retorno.split("\\")
    return{
        "nome": retornando[-1],
        "diretorio": retorno
    }

app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api-amazom")
async def read_root(busca: Buscar):
    Keywords = busca.Keywords.lower()
    SearchIndex = busca.SearchIndex.lower()
    ItemCount = busca.ItemCount

    response = Search(Keywords, SearchIndex, ItemCount)

    print(Keywords)
    # res = list(res)

    if response != "Error":
        return {"results": 200, "Mensagem": response}
    else:
        return {"Status": 404, "Mensagem":"Sem Resultados"}

