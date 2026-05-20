from django.conf import settings
from django.db import models
from django.urls import reverse


class PerfilUsuario(models.Model):
    SOLICITANTE = "SOLICITANTE"
    TECNICO = "TECNICO"
    COORDENADOR = "COORDENADOR"
    TIPOS = [
        (SOLICITANTE, "Solicitante"),
        (TECNICO, "Técnico"),
        (COORDENADOR, "Coordenador"),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default=SOLICITANTE)

    class Meta:
        verbose_name = "Perfil de usuário"
        verbose_name_plural = "Perfis de usuários"

    def __str__(self):
        return f"{self.usuario.username} ({self.get_tipo_display()})"

    @property
    def is_solicitante(self):
        return self.tipo == self.SOLICITANTE

    @property
    def is_tecnico(self):
        return self.tipo == self.TECNICO

    @property
    def is_coordenador(self):
        return self.tipo == self.COORDENADOR


class Laboratorio(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    bloco = models.CharField(max_length=20, blank=True)
    capacidade = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Chamado(models.Model):
    CATEGORIA_CHOICES = [
        ("HARDWARE", "Hardware"),
        ("SOFTWARE", "Software"),
        ("REDE", "Rede"),
        ("PROJETOR", "Projetor/Multimídia"),
        ("ACESSO", "Acesso/Login"),
        ("OUTROS", "Outros"),
    ]

    PRIORIDADE_CHOICES = [
        ("BAIXA", "Baixa"),
        ("MEDIA", "Média"),
        ("ALTA", "Alta"),
        ("CRITICA", "Crítica"),
    ]

    NOVO = "NOVO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"
    STATUS_CHOICES = [
        (NOVO, "Novo"),
        (EM_ANDAMENTO, "Em andamento"),
        (CONCLUIDO, "Concluído"),
        (CANCELADO, "Cancelado"),
    ]

    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    prioridade = models.CharField(
        max_length=10, choices=PRIORIDADE_CHOICES, default="MEDIA"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOVO)
    laboratorio = models.ForeignKey(
        Laboratorio, on_delete=models.PROTECT, related_name="chamados"
    )
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="chamados_abertos",
    )
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chamados_atribuidos",
    )
    anexo = models.FileField(upload_to="anexos/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"#{self.pk} {self.titulo}"

    def get_absolute_url(self):
        return reverse("chamados:detalhe", args=[self.pk])

    @property
    def tempo_atendimento_horas(self):
        if self.concluido_em:
            delta = self.concluido_em - self.criado_em
            return round(delta.total_seconds() / 3600, 2)
        return None


class Comentario(models.Model):
    chamado = models.ForeignKey(
        Chamado, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["criado_em"]

    def __str__(self):
        return f"Comentário #{self.pk} em #{self.chamado_id}"


class HistoricoStatus(models.Model):
    chamado = models.ForeignKey(
        Chamado, on_delete=models.CASCADE, related_name="historico"
    )
    de_status = models.CharField(max_length=20, blank=True)
    para_status = models.CharField(max_length=20)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["criado_em"]
        verbose_name = "Histórico de status"
        verbose_name_plural = "Histórico de status"

    def __str__(self):
        return f"#{self.chamado_id}: {self.de_status} -> {self.para_status}"
