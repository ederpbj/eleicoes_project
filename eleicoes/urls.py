from django.contrib import admin
from core import views  # Importe o arquivo de views da aplicação core
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),  # URLs do Dash
    path('', views.dashboard_view, name='dashboard'),  # Seu dashboard principal
]
