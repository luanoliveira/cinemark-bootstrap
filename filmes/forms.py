#coding: utf-8

from django import forms
from .widgets import ChannelWidget, TagInput
from django.core.exceptions import ValidationError

from datetime import datetime

def validators_date(value):
   try:
      datetime.strptime(value, "%Y")
   except Exception:
      raise ValidationError(
         '%(value)s is not an even number',
         params={'value': value},
      )

class FilmeForm(forms.Form):
   titulo = forms.CharField(
      label="Título", 
      max_length=150, 
      widget=forms.TextInput(attrs={'class': 'form-control'})
   )
   sinopse = forms.CharField(
      label="Sinopse", 
      widget=forms.Textarea(attrs={'class': 'form-control'})
   )
   ano_lancamento = forms.CharField(
      label="Ano de Lançamento",
      widget=forms.TextInput(attrs={'class': 'form-control'}),
      max_length=4,
      validators=[validators_date]
   )
   youtube = forms.CharField(
      label="Código do YouTube", 
      widget=forms.TextInput(attrs={'class': 'form-control'})
   )
   tags = forms.CharField(
      label="Tags",
      widget=TagInput()
   )
   capa = forms.ImageField()
   '''
   channels = forms.CharField(
      widget=ChannelWidget(),
      label="Canal",
   )
   '''
   #ano = forms.CharField(label="Ano de Lançamento", max_length=4)