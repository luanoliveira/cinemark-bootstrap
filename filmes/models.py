from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

import time

def validators_date(value):

      raise ValidationError(
         '%(value)s is not an even number',
         params={'value': value},
      )

# Create your models here.


def get_upload_path(instance, filename):
   return instance.path+str(time.time())+"."+filename.split(".")[-1]

class Tag(models.Model):
   titulo = models.CharField(max_length=100)

class Filme(models.Model):
   path = 'filmes/'

   titulo = models.CharField(max_length=150)
   sinopse = models.TextField()
   ano_lancamento = models.TextField(max_length=4, validators=[validators_date])
   youtube = models.TextField()
   tags = models.ManyToManyField(Tag)
   user = models.ForeignKey(User)
   #capa = models.ImageField(upload_to='filmes/%Y/%m/%d')
   capa = models.ImageField(upload_to=get_upload_path)  
