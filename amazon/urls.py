from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('products', view=views.get_all_product, name='get_all_product'),
    path('products/<str:name>', view=views.get_by_name, name='get_by_name'),
    path('asin/', view=views.get_by_asin, name='get_by_asin'),
    path('category', view=views.get_all_category, name='get_all_category'),
    path('category/<str:name>', view=views.get_by_category, name='get_by_category'),
]