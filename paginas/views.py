from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from cadastro.models import Residencia
from django.contrib.auth.models import User



#View do Painel admin
@login_required
def admin_dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('dashboard')
    return redirect('index')
    #return HttpResponseForbidden('Você Não Tem Permissão Para Acessar o Painel Administrador')


@login_required
def operador_dashboard(request):
    if request.user.groups.filter(name='Operador').exists():
        return render(request, 'paginas/operador/operador_dashboard.html')
    return redirect('index')


@login_required
def cliente_dashboard(request):
    if request.user.groups.filter(name='Cliente').exists():
        usuario_logado = request.user
        residencia = usuario_logado.residencia

        if hasattr(usuario_logado, "residencia") and hasattr(usuario_logado.residencia, "medicao"):

            medicao = usuario_logado.residencia.medicao.latest('data_hora') #acesso direto

            dados_medicao = {"energia_consumida_kwh": medicao.energia_consumida_kwh,
                             "energia_restante_kwh": medicao.energia_restante_kwh,
                             "energia_comprada_kwh": medicao.energia_comprada_kwh
                             }
        else:
            medicao = None
            dados_medicao = None #caso o usuario nao tenha medicao associada

        return render(request, 'paginas/cliente/cliente_dashboard.html', {'usuario': usuario_logado,
                                                                          "residencia": residencia, "medicao": dados_medicao,
                                                                          })
    return redirect('index')



class SucessoPagina(TemplateView):
    template_name = 'paginas/sucesso.html'


class ErroPagina(TemplateView):
    template_name = 'paginas/erro.html'


# Create your views here.
