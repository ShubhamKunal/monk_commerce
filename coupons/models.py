from django.db import models


# Create your models here.
class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=20,
        choices=[
            ("cart-wise", "cart-wise"),
            ("product-wise", "product-wise"),
            ("bxgy", "bxgy"),
        ]
    )
    details = models.JSONField()

    def __str__(self):
        return f"{self.type} coupon {self.id}"