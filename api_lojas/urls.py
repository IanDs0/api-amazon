from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', view=views.get_all_lojas, name='get_all_lojas'),
    path('amazon/', include('amazon.urls')),
]