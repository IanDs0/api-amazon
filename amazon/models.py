from django.db import models

# Create your models here.

class Asin(models.Model):
    asin_code = models.CharField(max_length=10, null=False, unique=True)

    def __str__(self) -> str:
        return f'Asin: {self.asin_code}'
