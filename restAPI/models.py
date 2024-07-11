from django.db import models

# Create your models here.
class Stocks(models.Model):
    symbol = models.CharField(max_length=30)
    def __str__(self):
        return f"Sym={self.symbol}"