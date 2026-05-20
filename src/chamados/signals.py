from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_perfil_automatico(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "perfil"):
        PerfilUsuario.objects.create(usuario=instance)
