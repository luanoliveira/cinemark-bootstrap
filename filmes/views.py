from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Filme
from .forms import FilmeForm

# Create your views here.
def list(request):

	formulario = FilmeForm(request.POST or None)

	if ( request.POST and formulario.is_valid() ):
		filme = Filme(
			titulo=formulario.cleaned_data["titulo"],
			sinopse=formulario.cleaned_data["sinopse"],
			ano_lancamento=formulario.cleaned_data["ano_lancamento"],
			youtube=formulario.cleaned_data["youtube"]
		)
		filme.save()

		messages.success(request, 'Filme cadastrado com sucesso.')
		return redirect('filmes')

	data = {
		"formulario": formulario, 
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