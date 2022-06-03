from django.db import models

from account.models import Account


CATEGORY_CHOICES=(  (0, "Automóveis"), 
                (1, "Ferramentas"),
                (2, "Roupa"),
                (3, "Imóveis"),
                (4, "Eletrodomésticos"),
                (5, "Desporto"),
                (6, "Tecnologia"),
                (7, "Lazer"),
                (8, "Móveis"),
                (9, "Outros"))

class Advertisement(models.Model):
    id          = models.AutoField(primary_key=True)
    seller      = models.ForeignKey(Account, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    img         = models.ImageField(null=True, blank=True, max_length=1024)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    promoted    = models.BooleanField(default=False)
    negotiable  = models.BooleanField(default=False)
    category    = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, null=True, blank=True)
    location    = models.CharField(max_length=100, null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True)
