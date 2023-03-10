from rest_framework import serializers

from .models import Loja, Category, Product, Price

class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        exclude = ['id']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']



class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = ['id']
        # fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    # product_loja = LojaSerializer()
    # product_category = CategorySerializer()
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