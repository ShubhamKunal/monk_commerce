from django.db import models
from products.models import Product
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return f"Cart {self.id}"