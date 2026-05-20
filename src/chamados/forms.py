import os

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Chamado, Comentario, PerfilUsuario

User = get_user_model()


class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
            "titulo",
            "descricao",
            "categoria",
            "prioridade",
            "laboratorio",
            "anexo",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "maxlength": 120}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "prioridade": forms.Select(attrs={"class": "form-select"}),
            "laboratorio": forms.Select(attrs={"class": "form-select"}),
            "anexo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_anexo(self):
        anexo = self.cleaned_data.get("anexo")
        if not anexo:
            return anexo
        ext = os.path.splitext(anexo.name)[1].lower()
        if ext not in settings.ANEXO_EXTENSOES_PERMITIDAS:
            raise forms.ValidationError(
                f"Extensão não permitida. Use: {', '.join(settings.ANEXO_EXTENSOES_PERMITIDAS)}"
            )
        if anexo.size > settings.MAX_ANEXO_BYTES:
            raise forms.ValidationError(
                f"Arquivo excede {settings.MAX_ANEXO_BYTES // (1024 * 1024)}MB."
            )
        return anexo

    def clean_titulo(self):
        return self.cleaned_data["titulo"].strip()


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Escreva um comentário..."}
            ),
        }


class AtribuirTecnicoForm(forms.Form):
    tecnico = forms.ModelChoiceField(
        queryset=User.objects.filter(perfil__tipo=PerfilUsuario.TECNICO),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Técnico responsável",
    )


class MudarStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=Chamado.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
