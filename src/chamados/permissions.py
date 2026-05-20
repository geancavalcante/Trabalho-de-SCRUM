from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import PerfilUsuario


def _tipo_usuario(user):
    if not user.is_authenticated:
        return None
    if hasattr(user, "perfil"):
        return user.perfil.tipo
    return None


def perfil_required(*tipos_permitidos):
    """Decorator que restringe a view a perfis específicos."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            tipo = _tipo_usuario(request.user)
            if tipo not in tipos_permitidos and not request.user.is_superuser:
                raise PermissionDenied("Seu perfil não tem permissão para esta ação.")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


def chamados_visiveis_para(user):
    """Retorna queryset de Chamado filtrado pelo perfil do usuário."""
    from .models import Chamado

    if user.is_superuser:
        return Chamado.objects.all()

    tipo = _tipo_usuario(user)
    if tipo == PerfilUsuario.COORDENADOR:
        return Chamado.objects.all()
    if tipo == PerfilUsuario.TECNICO:
        return Chamado.objects.filter(tecnico=user)
    if tipo == PerfilUsuario.SOLICITANTE:
        return Chamado.objects.filter(solicitante=user)
    return Chamado.objects.none()


def pode_alterar_status(user, chamado):
    if user.is_superuser:
        return True
    tipo = _tipo_usuario(user)
    if tipo == PerfilUsuario.COORDENADOR:
        return True
    if tipo == PerfilUsuario.TECNICO and chamado.tecnico_id == user.id:
        return True
    return False


def pode_comentar(user, chamado):
    if user.is_superuser:
        return True
    tipo = _tipo_usuario(user)
    if tipo == PerfilUsuario.COORDENADOR:
        return True
    if tipo == PerfilUsuario.TECNICO and chamado.tecnico_id == user.id:
        return True
    if tipo == PerfilUsuario.SOLICITANTE and chamado.solicitante_id == user.id:
        return True
    return False
