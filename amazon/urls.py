from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:name>', view=views.get_by_name, name='get_by_name'),
    path('asin/', view=views.get_by_asin, name='get_by_asin'),
]