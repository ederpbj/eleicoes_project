from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import Group

class RedirectLoggedInUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que não devem ser acessadas por usuários autenticados
        login_url = reverse('login')
        index_url = reverse('index')  # Página inicial padrão
        documentos_url = reverse('listar_documentos')
        admin_dashboard_url = reverse('admin_dashboard')

        # Se o usuário estiver autenticado e tentar acessar a página de login ou a página inicial
        if request.user.is_authenticated:
            # Verifica se o usuário está no grupo "Cadastrado"
            if request.user.groups.filter(name='Cadastrado').exists():
                # Redireciona o usuário "Cadastrado" para a página de aprovação caso tente acessar páginas restritas
                restricted_urls = [login_url, index_url, documentos_url, admin_dashboard_url]
                if request.path in restricted_urls:
                    return redirect('aguarde_aprovacao')

            # Caso o usuário não esteja no grupo "Cadastrado", segue a lógica padrão de redirecionamento
            if request.path in [login_url, index_url]:
                # Verifica se o usuário pertence ao grupo "Admin"
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('admin_dashboard')  # Redireciona para o dashboard do Admin
                else:
                    return redirect('listar_documentos')  # Redireciona para a página de documentos

        # Continua normalmente se não houver nenhuma condição que impeça o acesso
        response = self.get_response(request)
        return response
