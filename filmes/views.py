from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Filme, Tag
from .forms import FilmeForm
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from django.conf import settings

import os
from PIL import Image, ImageOps

import pprint

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.models import User

from django.views.generic import ListView


def cortar(media, width, height):
   media_path = os.path.join(settings.MEDIA_ROOT, media)
   
   size = (width, height)

   image = Image.open(media_path)

   image = ImageOps.fit(image, size, Image.ANTIALIAS)

   name_path = str(size[0])+"x"+str(size[1])
   path = os.path.dirname(media_path)+"/"+name_path

   if ( not os.path.exists(path) ):
      os.mkdir(path, 0755)

   image.save(os.path.join(path, os.path.basename(media_path)))


@login_required
def index(request):
   
   filmes = Filme.objects.all().filter(user=User.objects.get(pk=request.user.pk))
      
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
   
   if ( filme.capa ):
      formulario['capa'].field.required = False
   
   if ( request.POST ):

      formulario = FilmeForm(request.POST, request.FILES)

      if ( filme.capa ):
         formulario['capa'].field.required = False

      if ( formulario.is_valid() ):
         
         filme.titulo = request.POST["titulo"]
         filme.sinopse = request.POST["sinopse"]
         filme.ano_lancamento = request.POST["ano_lancamento"]
         filme.youtube = request.POST["youtube"]
         filme.user = User.objects.get(pk=request.user.pk)

         if ( 'capa' in request.FILES ):
            filme.capa=request.FILES['capa']
         
         filme.save()

         if ( filme.capa ):
            cortar(filme.capa.name, 250, 320)

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

      formulario = FilmeForm(request.POST, request.FILES)

      if ( formulario.is_valid() ):
         filme = Filme(
            titulo=request.POST["titulo"],
            sinopse=request.POST["sinopse"],
            ano_lancamento=request.POST["ano_lancamento"],
            youtube=request.POST["youtube"],
            capa=request.FILES['capa'],
            user=User.objects.get(pk=request.user.pk)
         )

         filme.save()

         if ( filme.capa ):
            cortar(filme.capa.name, 250, 320)

         for tag in formulario.cleaned_data["tags"].split(","):
               
            try:
               model_tag = Tag.objects.get(titulo=tag)
               filme.tags.add(model_tag)
            except:
               filme.tags.add(Tag.objects.create(titulo=tag))
            
         messages.success(request, 'Filme cadastrado com sucesso.')
         return redirect('filmes.create')
      
      return render(request, 'filmes/create.html', {
         "formulario": formulario
      });

   return redirect('filmes.index')

class HomeList(ListView):
   model = Filme
   template_name = 'home.html'

   def get_context_data(self, **kwargs):
      context = super(HomeList, self).get_context_data(**kwargs)
      context['nome_do_cara'] = 'Luan da Silva Oliveira'
      return context

class FilmeDelete(DeleteView):
   model = Filme
   success_url = reverse_lazy('filmes.index')
   success_message = 'Filme deletado com sucesso.'

   def delete(self, request, *args, **kwargs):
      messages.success(self.request, self.success_message)
      return super(FilmeDelete, self).delete(request, *args, **kwargs)