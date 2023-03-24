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
    try:
        existing_product = Product.objects.get(product_store_id=product['product_store_id'])
        old_price = existing_product.product_price
        existing_product.product_old_price = old_price
        existing_product.product_price = product['product_price']
        existing_product.save()
    except Product.DoesNotExist:
        serializer = ProductSerializer(data=product)
        if serializer.is_valid():
            serializer.save()
            existing_product = serializer.instance
            old_price = existing_product.product_price
            existing_product.product_old_price = old_price
            existing_product.save()
        else:
            print(serializer.errors)
            return False
    
    data_price = {
        'price_product': existing_product.id,
        'price_value': existing_product.product_price
    }
    serializer = PriceSerializer(data=data_price)
    if serializer.is_valid():
        serializer.save()
        product['product_old_price'] = existing_product.product_price
        return True
    else:
        print(serializer.errors)
        return False

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