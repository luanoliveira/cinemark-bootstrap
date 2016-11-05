#coding: utf-8

from django import forms
from .widgets import ChannelWidget, TagInput

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
   ano_lancamento = forms.DateField(
      label="Ano de Lançamento",
      input_formats=['%Y'],
      widget=forms.DateInput(attrs={'class': 'form-control'})
   )
   youtube = forms.CharField(
      label="Código do YouTube", 
      widget=forms.TextInput(attrs={'class': 'form-control'})
   )
   tags = forms.CharField(
      label="Tags",
      widget=TagInput()
   )
   '''
   channels = forms.CharField(
      widget=ChannelWidget(),
      label="Canal",
   )
   '''
   #ano = forms.CharField(label="Ano de Lançamento", max_length=4)