from historico.models import HistoricoEnergia
from cadastro.models import Residencia
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.


@login_required# Para garantir que  operação seja feita por um usuario logado
# Para garantir que o usuario logado tenha a permissão necessaeria
def lista_historico(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists() or request.user.groups.filter(name='Cliente').exists():
        # Filtra os usuarios que pertencem ao grupo Operador
        historico = HistoricoEnergia.objects.all()

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, numero_residenica, nome_proprietario, endereço
            historico = historico.filter(
                Q(data_transacao__icontains=search) | Q(valor_energia_kzs__icontains=search)
            )
        return render(request, 'historico/tabela_historico.html', {'historico': historico, 'search': search})
    else:
        return HttpResponseForbidden('Erro')


@login_required
def detalhes(request, historico_id):
    detalhes = get_object_or_404(HistoricoEnergia, id=historico_id)
    usuario = get_object_or_404(User, id=detalhes.usuario.id)
    if detalhes.usuario == request.user or request.user.groups.filter(name__in=["Admin", "Operdor"]).exists():
        return render(request, 'historico/detalhes.html', {"detalhes": detalhes, "usuario":usuario})
    return redirect('index')

