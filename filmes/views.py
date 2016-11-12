from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Filme, Tag
from .forms import FilmeForm
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from django.conf import settings

import os
from PIL import Image


def cortar(image, width, height):
   file = Image.open(image)

   original = (file.size[0], file.size[1])

   file = file.resize((original[1]*height/original[0], height), Image.ANTIALIAS)
   
   file = file.crop((0, 0, width, height))
   
   file.save(os.path.join(os.path.dirname(image), str(width)+"x"+str(height)+"_"+os.path.basename(image)))




@login_required
def index(request):
   
   filmes = Filme.objects.all()
      
   paginator = Paginator(filmes, 5)
   #print( request.user )

   page = request.GET.get('page')
   try:
      filmes = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      filmes = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      filmes = paginator.page(paginator.num_pages)

   data = {
      "filmes": filmes
   }

   return render(request, 'filmes/index.html', data)

@login_required
def store(request):
   print( request.POST )
   return render(request, 'filmes/store.html')

@login_required
def view(request, id):
   data = {
      "filme": Filme.objects.get(pk=id)
   }
   
   return render(request, 'filmes/view.html', data)

@login_required
def create(request):
   data = {
      "formulario": FilmeForm()
   }
   return render(request, 'filmes/create.html', data)

@login_required
def edit(request, pk):
   filme = Filme.objects.get(pk=pk)
   
   formulario = FilmeForm(model_to_dict(filme))

   if ( request.POST and request.FILES ):

      formulario = FilmeForm(request.POST, request.FILES)

      if ( formulario.is_valid() ):
         
         filme.titulo=formulario.cleaned_data["titulo"]
         filme.sinopse=formulario.cleaned_data["sinopse"]
         filme.ano_lancamento=formulario.cleaned_data["ano_lancamento"]
         filme.youtube=formulario.cleaned_data["youtube"]
         filme.capa=request.FILES['capa']
         
         filme.save()

         if ( filme.tags.all() ):
            #filme.tags.delete()
            filme.tags.clear()

         for tag in formulario.cleaned_data["tags"].split(","):
               
            try:
               model_tag = Tag.objects.get(titulo=tag)
               filme.tags.add(model_tag)
            except:
               filme.tags.add(Tag.objects.create(titulo=tag))

         messages.success(request, 'Filme cadastrado com sucesso.')
         return redirect('filmes.edit', pk=pk)

   return render(request, 'filmes/edit.html', {
      "filme": filme,
      "formulario": formulario
   })

@login_required
def store(request):
      
   if ( request.POST ):

      '''
      if ( 'capa' in request.FILES ):
         capa = os.path.join(settings.BASE_DIR, 'media/filmes/'+request.FILES['capa'].name)
         
         f = request.FILES['capa'].read()

         with open(capa, 'wb+') as destination:
            for chunk in request.FILES['capa'].chunks():
               destination.write(chunk)
         #print( request.FILES['capa'].read() )
      '''

      formulario = FilmeForm(request.POST, request.FILES)

      if ( formulario.is_valid() ):
         filme = Filme(
            titulo=formulario.cleaned_data["titulo"],
            sinopse=formulario.cleaned_data["sinopse"],
            ano_lancamento=formulario.cleaned_data["ano_lancamento"],
            youtube=formulario.cleaned_data["youtube"],
            capa=request.FILES['capa']
         )

         filme.save()

         if ( filme.capa ):
            #filmes/2016/11/12/602x0_1439644246_ZRh0dNf.jpg
            capa = os.path.join(settings.MEDIA_ROOT, filme.capa.name)

            cortar(capa, 200, 200)
            
         #print( filme.capa )

         for tag in formulario.cleaned_data["tags"].split(","):
               
            try:
               model_tag = Tag.objects.get(titulo=tag)
               filme.tags.add(model_tag)
            except:
               filme.tags.add(Tag.objects.create(titulo=tag))
            
         #messages.success(request, 'Filme cadastrado com sucesso.')
         #return redirect('filmes.create')
      
      return render(request, 'filmes/create.html', {
         "formulario": formulario
      });

   return redirect('filmes.index')





   