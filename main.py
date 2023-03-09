from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
from typing import Union
import threading
import schedule

from src.amazon import Search
from src.schedule import minha_rotina, thread_rotina


schedule.every(8).hours.do(minha_rotina)

thread = threading.Thread(target=thread_rotina)
thread.start()


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

        if response.errors is not None:
            return {"Status": response.erros[0].code, "Mensagem": response.erros}
        else:
            return {"results": 200, "Mensagem": response.search_result}

    except:
        print("ok")
        return {"Status": 400, "Mensagem": 'ItemCount é um valor não numérico'}