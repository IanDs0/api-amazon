from django.contrib import admin

from .models import Loja, Category, Product, Price

admin.site.register([Loja, Category, Product, Price])
