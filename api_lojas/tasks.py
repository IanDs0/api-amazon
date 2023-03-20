# from demoapp.models import Widget

from celery import shared_task

from amazon.search import search_asin

from api_lojas.models import Loja, Category, Product, Price
from api_lojas.serializers import LojaSerializer, CategorySerializer, ProductSerializer, ProductDetailSerializer, PriceSerializer, PriceDetailSerializer

from amazon.models import Asin
from amazon.serializers import AsinSerializer

def normalize_registration_product(product):

    loja = Loja.objects.get(loja_name=product['product_loja'])
    product['product_loja'] = loja.pk
    category = Category.objects.get_or_create(category_name=product['product_category'])
    product['product_category'] = category[0].id

    return(product)

def criate_price_for_product(product):

    data_product = product
    price = data_product.pop('product_price')
    serializer = ProductSerializer(data=data_product)
    if not serializer.is_valid():
        print(serializer.errors)
        return False
    if serializer.is_valid():
        prodc = Product.objects.get_or_create(**serializer.validated_data)

        data_price = {
            'price_product': prodc[0].id,
            'price_value': price
        }
        serializer = PriceSerializer(data=data_price)
        if not serializer.is_valid():
            print(serializer.errors)
        if serializer.is_valid():
            price = serializer.save()
            # prices = Price.objects.get_or_create(**serializer.validated_data)

def amazon():

    # asind e exempos "059035342X", "B0942NDQKL" e "B00ZV9RDKK"
    asin = []

    for ASIN in Asin.objects.all():
        asin.append(ASIN.asin_code)

    print(asin)

    if asin:

        try:

            response = search_asin(asin)
            responses={
                'response':[]
            }

            for i in range(len(response.items_result['Products'])):
                responses['response'].append(normalize_registration_product(response.items_result['Products'][i]))
                criate_price_for_product(responses['response'][i])

            if response.errors != None:
                return "Erro API Amazon " + str(response.errors[0].code)
            
        except:
            return "Erro ao buscar produtos na Amazon"
        
        return "OK"
    else:
        return "Nenhum ASIN cadastrado"

@shared_task
def map_products():

    store = {
        'amazon': amazon()
    }

    return store