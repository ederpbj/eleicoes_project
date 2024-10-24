# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('locais/', views.listar_locais, name='listar_locais'),
    path('locais/editar/<int:id>/', views.editar_local, name='editar_local'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
