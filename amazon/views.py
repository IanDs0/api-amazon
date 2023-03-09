from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api_lojas.models import Loja, Category, Product, Price
from api_lojas.serializers import LojaSerializer, CategorySerializer, ProductSerializer, ProductDetailSerializer, PriceSerializer, PriceDetailSerializer
from .search import Search

import json

@api_view(['GET'])
def get_by_name(request, name):

    searchindex = "All"
    itemcount = 1

    if request.method == 'GET':
        try:
            product = Product.objects.filter(product_name=name.replace('-', ' '))

            serializer = ProductDetailSerializer(product, many=True)

            if (request.GET['searchindex'] and request.GET['searchindex'] is not None) and (request.GET['itemcount'] and request.GET['itemcount'] is not None):
                searchindex = request.GET['searchindex'] if request.GET['searchindex'] is not None and request.GET['searchindex'] != '' else 'All'
                itemcount = request.GET['itemcount'] if request.GET['itemcount'] is not None and request.GET['itemcount'] !='' else 1


        except:
            return Response(serializer.data)
        
        if serializer.data == []:

            try:
                response = Search(name.replace('-', ' '), str(searchindex), int(itemcount))
                
                print(response)

                if response.errors != None:
                    return Response(status=response.errors[0].code)
            
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data)
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    
@api_view(['GET'])
def get_by_asin(request, asin):

    if request.method == 'GET':
        try:
            product = Product.objects.get(product_store_id=asin)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductDetailSerializer(product)

        return Response(serializer.data)