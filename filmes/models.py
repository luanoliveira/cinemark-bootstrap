from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Filme(models.Model):
    titulo = models.CharField(max_length=150)
    sinopse = models.TextField()
    ano_lancamento = models.DateField()