from django.db import models

from account.models import Account


CATEGORY_CHOICES=(  ("Automóveis", "Automóveis"), 
                ("Ferramentas", "Ferramentas"),
                ("Roupa", "Roupa"),
                ("Imóveis", "Imóveis"),
                ("Eletrodomésticos", "Eletrodomésticos"),
                ("Desporto", "Desporto"),
                ("Tecnologia", "Tecnologia"),
                ("Lazer", "Lazer"),
                ("Móveis", "Móveis"),
                ("Outros", "Outros"))

class Advertisement(models.Model):
    id          = models.AutoField(primary_key=True)
    seller      = models.ForeignKey(Account, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    img         = models.ImageField(null=True, blank=True, max_length=1024)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    promoted    = models.BooleanField(default=False)
    negotiable  = models.BooleanField(default=False)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    location    = models.CharField(max_length=100, null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True)
