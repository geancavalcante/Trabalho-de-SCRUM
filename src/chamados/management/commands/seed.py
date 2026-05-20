from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from chamados.models import (
    Chamado,
    HistoricoStatus,
    Laboratorio,
    PerfilUsuario,
)

User = get_user_model()

DEMO_PASSWORD = "Demo@2026"

USUARIOS = [
    ("solicitante1", "Ana", "Souza", "solicitante1@example.local", PerfilUsuario.SOLICITANTE),
    ("tecnico1", "Bruno", "Lima", "tecnico1@example.local", PerfilUsuario.TECNICO),
    ("coordenador1", "Carla", "Mendes", "coordenador1@example.local", PerfilUsuario.COORDENADOR),
]

LABS = [
    {"nome": "Lab Redes", "bloco": "B1", "capacidade": 30},
    {"nome": "Lab Software", "bloco": "B2", "capacidade": 25},
    {"nome": "Lab Hardware", "bloco": "B3", "capacidade": 20},
]


class Command(BaseCommand):
    help = "Cria dados iniciais para demonstração do Helpdesk Labs."

    @transaction.atomic
    def handle(self, *args, **options):
        criados = {}
        for username, first, last, email, tipo in USUARIOS:
            user, novo = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first, "last_name": last, "email": email},
            )
            if novo:
                user.set_password(DEMO_PASSWORD)
                user.save()
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.tipo = tipo
            perfil.save()
            criados[username] = user
            self.stdout.write(
                self.style.SUCCESS(f"Usuário {username} ({tipo}) {'criado' if novo else 'atualizado'}.")
            )

        labs = {}
        for dados in LABS:
            lab, novo = Laboratorio.objects.get_or_create(
                nome=dados["nome"], defaults={"bloco": dados["bloco"], "capacidade": dados["capacidade"]}
            )
            labs[dados["nome"]] = lab
            self.stdout.write(
                self.style.SUCCESS(f"Laboratório {dados['nome']} {'criado' if novo else 'existente'}.")
            )

        if Chamado.objects.count() == 0:
            ch1 = Chamado.objects.create(
                titulo="Projetor não liga na sala B2",
                descricao="O projetor não responde ao controle nem ao botão físico.",
                categoria="PROJETOR",
                prioridade="ALTA",
                status=Chamado.NOVO,
                laboratorio=labs["Lab Software"],
                solicitante=criados["solicitante1"],
            )
            HistoricoStatus.objects.create(
                chamado=ch1, de_status="", para_status=ch1.status, autor=criados["solicitante1"]
            )

            ch2 = Chamado.objects.create(
                titulo="Sem acesso à rede no Lab Redes",
                descricao="Estações sem DHCP. Cabo testado, switch parece OK.",
                categoria="REDE",
                prioridade="CRITICA",
                status=Chamado.EM_ANDAMENTO,
                laboratorio=labs["Lab Redes"],
                solicitante=criados["solicitante1"],
                tecnico=criados["tecnico1"],
            )
            HistoricoStatus.objects.create(
                chamado=ch2, de_status="", para_status=Chamado.NOVO, autor=criados["solicitante1"]
            )
            HistoricoStatus.objects.create(
                chamado=ch2, de_status=Chamado.NOVO, para_status=Chamado.EM_ANDAMENTO, autor=criados["coordenador1"]
            )

            ch3 = Chamado.objects.create(
                titulo="Software de simulação travando",
                descricao="O software trava ao abrir projetos > 200MB.",
                categoria="SOFTWARE",
                prioridade="MEDIA",
                status=Chamado.CONCLUIDO,
                laboratorio=labs["Lab Hardware"],
                solicitante=criados["solicitante1"],
                tecnico=criados["tecnico1"],
            )
            HistoricoStatus.objects.create(
                chamado=ch3, de_status="", para_status=Chamado.NOVO, autor=criados["solicitante1"]
            )
            HistoricoStatus.objects.create(
                chamado=ch3, de_status=Chamado.NOVO, para_status=Chamado.EM_ANDAMENTO, autor=criados["coordenador1"]
            )
            HistoricoStatus.objects.create(
                chamado=ch3, de_status=Chamado.EM_ANDAMENTO, para_status=Chamado.CONCLUIDO, autor=criados["tecnico1"]
            )
            from django.utils import timezone
            from datetime import timedelta
            ch3.concluido_em = ch3.criado_em + timedelta(hours=8)
            ch3.save()

            self.stdout.write(self.style.SUCCESS("3 chamados de exemplo criados."))
        else:
            self.stdout.write(self.style.WARNING("Chamados já existem — pulando criação de exemplos."))

        self.stdout.write(self.style.SUCCESS("Seed concluído. Senha dev: Demo@2026"))
