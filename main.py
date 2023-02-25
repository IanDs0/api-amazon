from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from src.amazon import Search


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
    return {"results": 200, "message": "API On"}

@app.get("/api-amazom/{search}")
async def read_root(search: str, searchindex: Union[str, None] = None, itemcount: Union[str, None] = None):
    keywords = search.replace('-', ' ')
    searchIndex = searchindex if searchindex is not None and searchindex != '' else 'All'
    itemCount = itemcount if itemcount is not None and itemcount !='' else 1

    try:
        itemCount = int(itemCount)

        response = (Search(keywords, searchIndex, itemCount))

        print(type(response))

        if response.errors is not None:
            return {"Status": response.erros[0].code, "Mensagem": response.erros}
        else:
            return {"results": 200, "Mensagem": response.search_result}

    except:
        print("ok")
        return {"Status": 400, "Mensagem": 'ItemCount é um valor não numérico'}