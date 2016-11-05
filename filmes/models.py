from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Tag(models.Model):
    titulo = models.CharField(max_length=100)

class Filme(models.Model):
    titulo = models.CharField(max_length=150)
    sinopse = models.TextField()
    ano_lancamento = models.DateField()
    youtube = models.TextField()
    tags = models.ManyToManyField(Tag)

