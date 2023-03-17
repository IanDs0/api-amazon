from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api_lojas.models import Loja, Category, Product, Price
from api_lojas.serializers import LojaSerializer, CategorySerializer, ProductSerializer, ProductDetailSerializer, PriceSerializer, PriceDetailSerializer
from .search import search_name, search_asin

import json

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
        print(prodc[0].id)

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
            print(price.id)


@api_view(['GET'])
def get_by_name(request, name):

    if request.method == 'GET':
        try:
            product = Product.objects.filter(product_name=name.replace('-', ' '))

            serializer = ProductDetailSerializer(product, many=True)

        except:
            return Response(serializer.data)
        
        if serializer.data == []:

            try:
                
                searchindex = request.GET.get('searchindex', 'All')
                itemcount = request.GET.get('itemcount', 1)

                response = search_name(name.replace('-', ' '), str(searchindex), int(itemcount))
                responses={
                    'response':[]
                }

                for i in range(len(response.search_result['Products'])):
                    responses['response'].append(normalize_registration_product(response.search_result['Products'][i]))
                
                if response.errors != None:
                    return Response(status=response.errors[0].code)
                
                serializer = ProductSerializer(responses, many=True)
            
            except Exception as e:
                print(e)
                return Response(status=response)

            return Response(data=responses['response'], status=200)
        
        return Response(serializer.data)

    
@api_view(['GET','POST'])
def get_by_asin(request):

    if request.method == 'GET':

        prduct_asin = request.GET.get('prduct', '')
        if prduct_asin != '':
            product = Product.objects.get(product_store_id = prduct_asin)
            prices = Price.objects.filter(price_product = product.id)
            
            try:
                serializer = PriceSerializer(prices, many=True)
                return Response(serializer.data)
            except:
                return Response(status= status.HTTP_400_BAD_REQUEST)

        return Response(status= status.HTTP_404_NOT_FOUND)


    if request.method == 'POST':
        
        if request.data['asin'] != [] and type(request.data['asin']) == type([]):

            try:

                response = search_asin(request.data['asin'])
                responses={
                    'response':[]
                }
                res = []

                for i in range(len(response.items_result['Products'])):
                    responses['response'].append(normalize_registration_product(response.items_result['Products'][i]))
                    criate_price_for_product(responses['response'][i])

                if response.errors != None:
                    return Response(status=response.errors[0].code)
                
            
            except:
                return Response(status=response)
            
            serializer = ProductSerializer(responses, many=True)
            # print(serializer)

            return Response(data=responses['response'], status=200)
        
        return Response(serializer.data)