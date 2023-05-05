from rest_framework.test import APITestCase
from rest_framework import status

from api_lojas.models import Loja, Category, Product, Price

import json

STORIES_URL = '/amazon/'
STORIES_URL_PRODUCTS = STORIES_URL+'products'
STORIES_URL_PRODUCT = STORIES_URL_PRODUCTS+'/teste'
STORIES_URL_CATEGORY = STORIES_URL+'category'
STORIES_URL_PRODUCTS_CATEGORY = STORIES_URL_CATEGORY+'/teste'
STORIES_URL_REGISTER_STORE_ID = STORIES_URL+'asin/'
STORIES_URL_STORE_ID = STORIES_URL_REGISTER_STORE_ID+'?prduct=asdf'


class MeuTesteDeAPI(APITestCase):
    def setUp(self):
        self.loja = Loja.objects.create(pk=2, loja_color='f0f0f0', loja_name='loja_teste')
        self.category = Category.objects.create(pk=2, category_name='category_teste')
        self.product = Product.objects.create(
            pk=2, 
            product_store_id='asdf',
            product_name='product_teste', 
            product_url='http://teste.com',
            product_image_url='http://teste.com/img.jpg',
            product_price=10.55, 
            product_old_price=9.45,
            product_loja=self.loja,
            product_category=self.category
            )
        
        self.price = Price.objects.create(
            price_product=self.product,
            price_value=10.55,
            )
        self.price2 = Price.objects.create(
            price_product=self.product,
            price_value=10.55,
            )

    # def test_list_all_products(self):

    #     products = Product.objects.all()
    #     stories = Loja.objects.all()
    #     category = Category.objects.all()
    #     price = Price.objects.all()

    #     response = self.client.get(STORIES_URL_PRODUCTS)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     print(response)
    #     self.assertEqual(len(response.data), len(products))

        # i=0

        # for product in products:
        #     self.assertEqual(response.data[i]['loja_color'], product.loja_color)
        #     self.assertEqual(response.data[i]['loja_name'], product.loja_name)
        #     i+=1

    # def test_search_name_products(self):

    #     products = Product.objects.filter(product_name='product_teste')

    #     response = self.client.get('/amazon/products/product_teste')
    #     print(products)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, products[0])

    def test_price_product_by_store_id(self):

        product = Product.objects.get(product_store_id = "asdf")
        prices = Price.	objects.filter(price_product = product.id)

        response = self.client.get(STORIES_URL_STORE_ID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        i=0

        for products in response.data:
            self.assertEqual(
                float(products['price_value']), 
                float(prices[i].price_value)
                )
            # self.assertEqual(
            #     products['price_product'], 
            #     prices[i].price_product
            #     )
            self.assertEqual(
                products['price_date'], 
                prices[i].price_date
                )
            i+=1