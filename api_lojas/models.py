from django.db import models
from django.utils import timezone

# Create your models here.

class Loja(models.Model):
    loja_color = models.CharField(max_length=6, null=False, unique=True)
    loja_name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self) -> str:
        return f'Cor: #{self.loja_color}, \
            Name: {self.loja_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=25, null=False, unique=True)
    
    def __str__(self) -> str:
        return f'Nome: {self.category_name}'

class Product(models.Model):
    product_store_id = models.CharField(max_length=10, null=False)
    product_name = models.CharField(max_length=200, null=False)
    product_url = models.URLField(max_length=200, null=False)
    product_image_url = models.URLField(max_length=200, null=False)
    # product_description = models.TextField(null=False)
    product_loja = models.ForeignKey(Loja, on_delete=models.PROTECT, related_name='Products', null=False)
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='Products', null=False)

    def __str__(self) -> str:
        return f'Nome: {self.product_name}, \
            Store id: {self.product_store_id} \
            Url: {self.product_url}, \
            Imagem: {self.product_image_url}, \
            Loja: {self.product_loja}, \
            Categoria: {self.product_category}'

class Price(models.Model):
    price_product = models.ForeignKey(Product, on_delete=models.CASCADE, null= False)
    price_value = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    price_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'Produto: {self.price_product}, \
            Valor: {self.price_value}, \
            Data: {self.price_date}'

