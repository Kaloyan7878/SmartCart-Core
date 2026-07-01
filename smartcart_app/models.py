from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Име на продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (лв.)")
    barcode = models.CharField(max_length=50, unique=True, verbose_name="Баркод")
    stock = models.IntegerField(default=0, verbose_name="Наличност")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} лв."