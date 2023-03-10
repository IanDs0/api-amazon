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

    
@api_view(['POST'])
def get_by_asin(request):

    if request.method == 'POST':
        
        if request.data != []:

            try:

                response = search_asin(tuple(request.data))
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