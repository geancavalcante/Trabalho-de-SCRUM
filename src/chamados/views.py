import logging
from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AtribuirTecnicoForm,
    ChamadoForm,
    ComentarioForm,
    MudarStatusForm,
)
from .models import Chamado, HistoricoStatus, PerfilUsuario
from .permissions import (
    chamados_visiveis_para,
    perfil_required,
    pode_alterar_status,
    pode_comentar,
)

log = logging.getLogger("chamados")


@login_required
def dashboard(request):
    qs = chamados_visiveis_para(request.user)
    resumo = OrderedDict(
        (rotulo, qs.filter(status=valor).count())
        for valor, rotulo in Chamado.STATUS_CHOICES
    )
    recentes = qs.order_by("-criado_em")[:5]
    perfil = getattr(request.user, "perfil", None)
    return render(
        request,
        "chamados/dashboard.html",
        {
            "resumo": resumo,
            "recentes": recentes,
            "perfil": perfil,
            "total": qs.count(),
        },
    )


@login_required
def lista_chamados(request):
    qs = chamados_visiveis_para(request.user)
    status = request.GET.get("status")
    prioridade = request.GET.get("prioridade")
    categoria = request.GET.get("categoria")
    if status:
        qs = qs.filter(status=status)
    if prioridade:
        qs = qs.filter(prioridade=prioridade)
    if categoria:
        qs = qs.filter(categoria=categoria)
    qs = qs.select_related("laboratorio", "solicitante", "tecnico")
    return render(
        request,
        "chamados/chamado_list.html",
        {
            "chamados": qs,
            "status_atual": status or "",
            "prioridade_atual": prioridade or "",
            "categoria_atual": categoria or "",
            "status_choices": Chamado.STATUS_CHOICES,
            "prioridade_choices": Chamado.PRIORIDADE_CHOICES,
            "categoria_choices": Chamado.CATEGORIA_CHOICES,
        },
    )


@perfil_required(PerfilUsuario.SOLICITANTE, PerfilUsuario.COORDENADOR)
def criar_chamado(request):
    if request.method == "POST":
        form = ChamadoForm(request.POST, request.FILES)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.solicitante = request.user
            chamado.save()
            HistoricoStatus.objects.create(
                chamado=chamado,
                de_status="",
                para_status=chamado.status,
                autor=request.user,
            )
            log.info(
                "Chamado %s criado por %s (lab=%s, prioridade=%s)",
                chamado.pk,
                request.user.username,
                chamado.laboratorio_id,
                chamado.prioridade,
            )
            messages.success(request, f"Chamado #{chamado.pk} criado com sucesso.")
            return redirect(chamado.get_absolute_url())
    else:
        form = ChamadoForm()
    return render(request, "chamados/chamado_form.html", {"form": form})


@login_required
def detalhe_chamado(request, pk):
    chamado = get_object_or_404(
        Chamado.objects.select_related("laboratorio", "solicitante", "tecnico"),
        pk=pk,
    )
    if not chamados_visiveis_para(request.user).filter(pk=pk).exists():
        raise PermissionDenied("Você não tem acesso a este chamado.")

    comentario_form = ComentarioForm()
    status_form = MudarStatusForm(initial={"status": chamado.status})
    atribuir_form = AtribuirTecnicoForm(initial={"tecnico": chamado.tecnico})

    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "comentar":
            if not pode_comentar(request.user, chamado):
                raise PermissionDenied("Você não pode comentar este chamado.")
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                c = comentario_form.save(commit=False)
                c.chamado = chamado
                c.autor = request.user
                c.save()
                log.info(
                    "Comentário em chamado %s por %s", chamado.pk, request.user.username
                )
                messages.success(request, "Comentário adicionado.")
                return redirect(chamado.get_absolute_url())

        elif acao == "mudar_status":
            if not pode_alterar_status(request.user, chamado):
                raise PermissionDenied("Você não pode alterar o status.")
            status_form = MudarStatusForm(request.POST)
            if status_form.is_valid():
                novo = status_form.cleaned_data["status"]
                anterior = chamado.status
                if novo != anterior:
                    chamado.status = novo
                    if novo == Chamado.CONCLUIDO and not chamado.concluido_em:
                        chamado.concluido_em = timezone.now()
                    if novo != Chamado.CONCLUIDO:
                        chamado.concluido_em = None
                    chamado.save()
                    HistoricoStatus.objects.create(
                        chamado=chamado,
                        de_status=anterior,
                        para_status=novo,
                        autor=request.user,
                    )
                    log.info(
                        "Status do chamado %s alterado: %s -> %s por %s",
                        chamado.pk,
                        anterior,
                        novo,
                        request.user.username,
                    )
                    messages.success(
                        request, f"Status alterado para {chamado.get_status_display()}."
                    )
                return redirect(chamado.get_absolute_url())

        elif acao == "atribuir":
            if not (
                request.user.is_superuser
                or (hasattr(request.user, "perfil") and request.user.perfil.is_coordenador)
            ):
                raise PermissionDenied("Apenas coordenadores podem atribuir técnicos.")
            atribuir_form = AtribuirTecnicoForm(request.POST)
            if atribuir_form.is_valid():
                tecnico = atribuir_form.cleaned_data["tecnico"]
                chamado.tecnico = tecnico
                if chamado.status == Chamado.NOVO:
                    anterior = chamado.status
                    chamado.status = Chamado.EM_ANDAMENTO
                    HistoricoStatus.objects.create(
                        chamado=chamado,
                        de_status=anterior,
                        para_status=chamado.status,
                        autor=request.user,
                    )
                chamado.save()
                log.info(
                    "Chamado %s atribuído a %s por %s",
                    chamado.pk,
                    tecnico.username,
                    request.user.username,
                )
                messages.success(
                    request, f"Chamado atribuído a {tecnico.username}."
                )
                return redirect(chamado.get_absolute_url())

    comentarios = chamado.comentarios.select_related("autor")
    historico = chamado.historico.select_related("autor")
    return render(
        request,
        "chamados/chamado_detail.html",
        {
            "chamado": chamado,
            "comentarios": comentarios,
            "historico": historico,
            "comentario_form": comentario_form,
            "status_form": status_form,
            "atribuir_form": atribuir_form,
            "pode_comentar": pode_comentar(request.user, chamado),
            "pode_alterar_status": pode_alterar_status(request.user, chamado),
            "pode_atribuir": (
                request.user.is_superuser
                or (
                    hasattr(request.user, "perfil")
                    and request.user.perfil.is_coordenador
                )
            ),
        },
    )


@perfil_required(PerfilUsuario.COORDENADOR)
def relatorios(request):
    qs = Chamado.objects.all()
    por_categoria = (
        qs.values("categoria").annotate(total=Count("id")).order_by("-total")
    )
    por_laboratorio = (
        qs.values("laboratorio__nome").annotate(total=Count("id")).order_by("-total")
    )
    por_status = (
        qs.values("status").annotate(total=Count("id")).order_by("status")
    )
    concluidos = qs.filter(status=Chamado.CONCLUIDO, concluido_em__isnull=False)
    tempo_medio_horas = None
    if concluidos.exists():
        deltas = [
            (c.concluido_em - c.criado_em).total_seconds() / 3600 for c in concluidos
        ]
        tempo_medio_horas = round(sum(deltas) / len(deltas), 2)

    categoria_label = dict(Chamado.CATEGORIA_CHOICES)
    status_label = dict(Chamado.STATUS_CHOICES)
    return render(
        request,
        "chamados/relatorio.html",
        {
            "por_categoria": [
                {"nome": categoria_label.get(r["categoria"], r["categoria"]), "total": r["total"]}
                for r in por_categoria
            ],
            "por_laboratorio": por_laboratorio,
            "por_status": [
                {"nome": status_label.get(r["status"], r["status"]), "total": r["total"]}
                for r in por_status
            ],
            "tempo_medio_horas": tempo_medio_horas,
            "total": qs.count(),
        },
    )
