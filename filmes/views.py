from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Filme, Tag
from .forms import FilmeForm
from django.forms.models import model_to_dict

# Create your views here.
def index(request):

   data = {
      "filmes": Filme.objects.all()
   }

   return render(request, 'filmes/index.html', data)

def store(request):
   print( request.POST )
   return render(request, 'filmes/store.html')


def view(request, id):
   data = {
      "filme": Filme.objects.get(pk=id)
   }
   
   return render(request, 'filmes/view.html', data)

def create(request):
   data = {
      "formulario": FilmeForm()
   }
   return render(request, 'filmes/create.html', data)

def edit(request, pk):
   filme = Filme.objects.get(pk=pk)
   
   formulario = FilmeForm(model_to_dict(filme))

   if ( request.POST ):
      formulario = FilmeForm(request.POST)

      if ( formulario.is_valid() ):
         
         filme.titulo=formulario.cleaned_data["titulo"];
         filme.sinopse=formulario.cleaned_data["sinopse"];
         filme.ano_lancamento=formulario.cleaned_data["ano_lancamento"];
         filme.youtube=formulario.cleaned_data["youtube"];
         
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

def store(request):
      
   if ( request.POST ):

      formulario = FilmeForm(request.POST)

      if ( formulario.is_valid() ):
         filme = Filme(
            titulo=formulario.cleaned_data["titulo"],
            sinopse=formulario.cleaned_data["sinopse"],
            ano_lancamento=formulario.cleaned_data["ano_lancamento"],
            youtube=formulario.cleaned_data["youtube"]
         )

         filme.save()

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