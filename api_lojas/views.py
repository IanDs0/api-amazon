from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Loja
from .serializers import LojaSerializer

import json
# Create your views here.

@api_view(['GET'])
def get_all_lojas(request):


    if request.method == 'GET':
        stories = Loja.objects.all()

        serializer = LojaSerializer(stories, many=True)

        return Response(serializer.data)