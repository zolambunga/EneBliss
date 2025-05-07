'''
    O arquivo forms.py no Django é usado para definir formulários que permitem a criação,
    edição e validação de dados no sistema.Ele funciona como uma camada entre o modelo
    e a interface do usuário  criando um formulário que os usuários podem preencher em
    uma interface web. O django fornece dois tipos de formulários principais:

        1- Formulários simples(forms.Form): são usados para  criar formulário independentes
         dos modelos.
        2- Formulários baseados em modelos(forms.ModelForm): são usados quando  você deseja
          criar ou atualizar instancias de um modelo(fornecido) directamente apartir de um
          formulário

        Quando um formulário é enviado para o servidor (via POST), o Django valida automaticamente
        os dados usando as regras de validação definidas para os campos do formulário. Ex:
             CharField: Valida que o valor é uma string
             EmailFied: Valida que o valor é um endereço de email válido
             DateField: Valida que o valor seja uma data válida

        Após a validação, o formulário retorna um valor booleano indicando se os dados são válidos
        ou não, com o método is_valid(tipo de dados corretos e campos obrigatórios). Se os dados
        forem válidos o método form.save() salva a instancia do modelo associada ao formulário no
        banco de dados. Após a criação do post, o usuário é redirecionado para a página de listagem
        post.
        Obs: você pode acessar os dados submetidos via cleaned_data, que é um dicionário
        contendo os dados validos.

        Além da validação automática fornecida pelo django, você também pode definir validação
        personalizada dentro de um formulário. Isso pode ser feito usando o método clean_<campo>
        Dentro da class form criamos uma função:
            def clean_name(self):
                name = self.claned_data['name']
                if len(name) < 3:
                    raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
                return name
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # usado para editar formularios
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password #usado para criptografia
#from django.core.exceptions import ValidationError
from .models import PT, Post, Residencia

'''
Usaremos o modelo nativo do django User, pois já inclui grupos, então iremos referencia-lo
Criaremos o nosso próprio formulário com base no formulario padrao do django (forms.ModelForm),
'''


'''
Formulario De Administradores e Operadres Para Cadastrar PTS(Post de Transformação)
'''

class PTFormCreate(forms.ModelForm):

    class Meta:

        model = PT
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['nome_pt', 'numero_pt', 'municipio_pt', 'bairro_pt']



'''
Formulario De Admistradores e Operadores Para Cadastrar Posts
'''
class PostFormCreate(forms.ModelForm):

    class Meta:
        model = Post
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['pt', 'nome_post', 'numero_post', 'rua_post']


'''
Formulario de Admistradores e Operadores Para Criar Cadastros De residencias
 para usuarios do tipo cliente
'''
class ResidenciaFormCreate(forms.ModelForm):

    class Meta:
        model = Residencia
        fields = ['post', 'numero_residencia', 'nome_proprietario', 'endereco_residencia']



'''
Formulario Somente de Admistrador Para Criar Cadastros De Usuarios (admin, operadores e clientes)
este formulario AdminFormCreateUsuario permite apenas administrador cadastrar usuario para todos os grupos
'''
class AdminFormCreateUsuario(UserCreationForm):

    group = forms.ChoiceField(choices=[('Admin', 'Admin'), ('Operador', 'Operador')])

    class Meta:
        model = User
        fields = ['username', 'email', 'telefone', 'group', 'password1', 'password2', 'foto_perfil']

    #Sobrescrevendo o metodo save para adicionar o grupo ao usuario

    def save(self, commit=True):
        user = super().save(commit=False)
        group_name = self.cleaned_data['group']
        group = Group.objects.get(name=group_name)
        if commit:
            user.save()
            user.groups.add(group)
        return user

'''
Formulario Somente de Operadores Para Criar Cadastros De Usuarios (clientes) este formulario
OperadorFormCreateCliente permite o Operador logado cadastrar usuario somente para o grupo Cliente
'''


class OperadorFormCreateCliente(UserCreationForm):

    class Meta:
        model = User
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['username', 'email', 'telefone', 'password1', 'password2', 'foto_perfil']


        # o metodo save é sobrescristo para garantir que a senha do usuário seja criptografada
        # corretamente e que o usuário seja adicionado ao grupo selecionado
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            grupo_cliente = Group.objects.get(name='Cliente')
            user.groups.add(grupo_cliente)
        return user





'''
Formulario Somente de Admistrador Para Editar Cadastros De Usuarios (admin, operadores e clientes)
este formulario AdminFormCreateUsuario permite apenas administrador cadastrar usuario para todos os grupos
'''
class UsuarioFormUpdate(UserChangeForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label="")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label="")

    class Meta:
        model = User
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['username', 'email', 'telefone', 'password1', 'password2', 'foto_perfil']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("As senhas não coincidem.Tente novamente")

            # Criptografa a Senha antes de salvar
            # cleaned_data['password1'] = make_password(password1)
        return cleaned_data


'''
Formulario Somente de Operadores Para Editar Cadastros De Usuarios (clientes) este formulario
OperadorFormCreateCliente permite o Operador logado cadastrar usuario somente para o grupo Cliente
'''


class ClienteFormUpdate(UserChangeForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label="")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label="")

    class Meta:
        model = User
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['username', 'email', 'telefone', 'password1', 'password2', 'foto_perfil']


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("As senhas não coincidem.Tente novamente")

            # Criptografa a Senha antes de salvar
            #cleaned_data['password1'] = make_password(password1)
        return cleaned_data

'''
class ResidenciaFormUpdate(forms.ModelForm):

    class Meta:
            model = Residencia
            fields = ['numero_residencia', 'nome_proprietario']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Criptografando a Senha
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
'''




#####################Admistrador Editar Cadastros###################

class PTFormUpdate(UserCreationForm):
    class Meta:
        model = PT
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['nome_pt', 'numero_pt', 'municipio_pt', 'bairro_pt']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class PostFormUpdate(UserCreationForm):
    class Meta:
        model = Post
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['pt', 'numero_post', 'rua_post']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
