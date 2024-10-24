from django.contrib import admin
from django.urls import path
from core import views  # Importe o arquivo de views da aplicação core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='home'),  # Definir o dashboard como página principal
]

