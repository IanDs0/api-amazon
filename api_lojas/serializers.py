from rest_framework import serializers

from .models import Loja, Category, Product, Price

class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1



class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        depth = 1