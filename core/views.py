from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import LocalVotacao

def listar_locais(request):
    locais = LocalVotacao.objects.all()
    return render(request, 'eleicoes_app/listar_locais.html', {'locais': locais})

def editar_local(request, id):
    local = get_object_or_404(LocalVotacao, pk=id)
    if request.method == 'POST':
        local.nome_local = request.POST.get('nome_local')
        local.endereco = request.POST.get('endereco')
        # Adicione outros campos conforme necessário
        local.save()
        return redirect('listar_locais')
    return render(request, 'eleicoes_app/editar_local.html', {'local': local})

