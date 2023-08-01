from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.URLField()

    def __str__(self):
        return f'{self.user} - {self.name}'

