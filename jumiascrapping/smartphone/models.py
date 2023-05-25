from bs4 import BeautifulSoup
from django.db import models

# Create your models here.
from django.db import models
import requests

class Phone(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=100)
    link = models.CharField(max_length=200)

