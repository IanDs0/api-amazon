from .amazon import Search
import schedule
import time

produtos = [
    "Iphone 13",
    "Echo dot"
]
SearchIndex = "All"
ItemCount = "1"

# função que será executada em uma thread separada
def thread_rotina():
    while True:
        schedule.run_pending()
        time.sleep(1)

def minha_rotina():
    # aqui você pode colocar a tarefa que deseja executar em um intervalo de tempo específico
    for product in produtos:

        search = Search(product, SearchIndex, ItemCount)
        search.search()