from django.contrib import admin

from .models import (
    Chamado,
    Comentario,
    HistoricoStatus,
    Laboratorio,
    PerfilUsuario,
)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo")
    list_filter = ("tipo",)
    search_fields = ("usuario__username", "usuario__email")


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ("nome", "bloco", "capacidade")
    search_fields = ("nome", "bloco")


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0


class HistoricoStatusInline(admin.TabularInline):
    model = HistoricoStatus
    extra = 0
    readonly_fields = ("de_status", "para_status", "autor", "criado_em")


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "titulo",
        "categoria",
        "prioridade",
        "status",
        "laboratorio",
        "solicitante",
        "tecnico",
        "criado_em",
    )
    list_filter = ("status", "prioridade", "categoria", "laboratorio")
    search_fields = ("titulo", "descricao", "solicitante__username")
    inlines = [ComentarioInline, HistoricoStatusInline]
    readonly_fields = ("criado_em", "atualizado_em", "concluido_em")
