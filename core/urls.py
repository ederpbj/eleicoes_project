from django.contrib.auth import admin
from . import views
from django.urls import include, path

urlpatterns = [
    path('locais/', views.listar_locais, name='listar_locais'),
    path('locais/editar/<int:id>/', views.editar_local, name='editar_local'),

    # admin
    path('admin/', admin.site.urls),
    path('eleicoes/', include('eleicoes_app.urls')),
]
