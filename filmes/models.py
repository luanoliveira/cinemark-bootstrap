from __future__ import unicode_literals

from django.db import models

from django.core.exceptions import ValidationError

from datetime import datetime

def validators_date(value):

      raise ValidationError(
         '%(value)s is not an even number',
         params={'value': value},
      )

# Create your models here.

class Tag(models.Model):
    titulo = models.CharField(max_length=100)

class Filme(models.Model):
    titulo = models.CharField(max_length=150)
    sinopse = models.TextField()
    ano_lancamento = models.TextField(max_length=4, validators=[validators_date])
    youtube = models.TextField()
    tags = models.ManyToManyField(Tag)
