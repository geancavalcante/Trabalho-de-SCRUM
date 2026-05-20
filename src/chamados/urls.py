from django.urls import path

from . import views

app_name = "chamados"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("chamados/", views.lista_chamados, name="lista"),
    path("chamados/novo/", views.criar_chamado, name="criar"),
    path("chamados/<int:pk>/", views.detalhe_chamado, name="detalhe"),
    path("relatorios/", views.relatorios, name="relatorios"),
]
