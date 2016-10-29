#coding: utf-8

from django import forms

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
   #ano = forms.CharField(label="Ano de Lançamento", max_length=4)