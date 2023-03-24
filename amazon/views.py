from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api_lojas.models import Loja, Category, Product, Price
from api_lojas.serializers import LojaSerializer, CategorySerializer, ProductSerializer, ProductDetailSerializer, PriceSerializer, PriceDetailSerializer, PriceMinimalSerializer
from .search import search_name, search_asin

import json

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



@api_view(['GET'])
def get_all_product(request):
    if request.method == 'GET':
        try:
            stories = Loja.objects.filter(loja_name = 'amazon')
            if stories == []:
                return Response(status= status.HTTP_400_BAD_REQUEST)
            products = Product.objects.filter(product_loja = stories[0])
            products = products.order_by('-product_price')
            serializer = ProductDetailSerializer(products, many=True)
        except:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


@api_view(['GET'])
def get_all_category(request):
    if request.method == 'GET':
        try:
            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True)
        except:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

@api_view(['GET'])
def get_by_category(request, name):

    if request.method == 'GET':
        try:
            category = Category.objects.filter(category_name=name.replace('-', ' '))
            products = Product.objects.filter(product_category = category[0].id)
            serializer = ProductSerializer(products, many=True)
        except:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

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
            
            except:
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
                serializer = PriceMinimalSerializer(prices, many=True)
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
                    price=criate_price_for_product(responses['response'][i])
                    print(price)
                    # responses['response'][i]['product_old_price']=10.0

                if response.errors != None:
                    return Response(status=response.errors[0].code)
                
            
            except:
                return Response(status=response)
            
            serializer = ProductSerializer(responses, many=True)
            # print(serializer)

            return Response(data=responses['response'], status=200)
        
        return Response(serializer.data)