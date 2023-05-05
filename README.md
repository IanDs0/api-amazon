# API de Busca de Produtos da Amazon

## Rotas da API
GET `/`

- Retorna todas as lojas da API.

GET `/amazon/protudo-buscado?searchindex=category&itemcount=n`

- Retorna "n" produtos buscados da categoria "category" na Amazon.

- Os parâmetros searchindex e itemcount na URL não são obrigatórios.

- searchindex tem valor padrão de "all" e deve receber uma string.

- itemcount tem valor padrão de 1 e deve receber um inteiro.

POST `/amazon/asin/?prduct=p`

- Deve ter um "product" com o valor de um asin.

- Retorna o hitórico de precos do produto.

POST `/amazon/asin/`

- Deve ter um valor no body de nome "asin" que possua os valores na estrutura de dados array.

- Retorna os dados dos ASIN que estavam no array de busca e escreve esses produtos no banco.

## Dependências
- Python `3.11.2`

- SDK da Amazon utilizada
  - `cd ./SDK_Amazon/paapi5-python-sdk-example`
  - `python setup.py install`
- Dependências utilizadas
  - `pip install -r requirements.txt`
- Para executar o servidor na porta `8000`:
  - `python3 manage.py runserver 0.0.0.0:8000`
