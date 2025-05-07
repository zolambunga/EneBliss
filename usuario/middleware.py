'''
Atualiza o status sempre que um usuário entrar no sistema

'''

from django.utils.deprecation import MiddlewareMixin
import datetime

class StatusUsuarioMiddleware(MiddlewareMixin):

    def process_request(self, request):
        '''
            Atualiza o status do usuario quando ele faz uma requisição
        '''
        if request.user.is_authenticated:
            request.user.online = True # Define como online
            request.user.tempo_de_atividade = datetime.datetime.now() #Atualiza ultima actividade
            request.user.save()

    def process_response(self, request, response):
        if request.user.is_authenticated and not request.user.is_active:
            request.user.online = False
            request.user.save()
        return response
