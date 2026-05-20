from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Chamado, HistoricoStatus, Laboratorio, PerfilUsuario

User = get_user_model()


def criar_usuario(username, tipo):
    u = User.objects.create_user(username=username, password="Senha@123Teste")
    u.perfil.tipo = tipo
    u.perfil.save()
    return u


class FluxoChamadoTests(TestCase):
    def setUp(self):
        self.solicitante = criar_usuario("sol1", PerfilUsuario.SOLICITANTE)
        self.solicitante2 = criar_usuario("sol2", PerfilUsuario.SOLICITANTE)
        self.tecnico = criar_usuario("tec1", PerfilUsuario.TECNICO)
        self.tecnico2 = criar_usuario("tec2", PerfilUsuario.TECNICO)
        self.coord = criar_usuario("coord1", PerfilUsuario.COORDENADOR)
        self.lab = Laboratorio.objects.create(nome="Lab Teste", bloco="X1", capacidade=20)

    def test_solicitante_cria_chamado(self):
        self.client.login(username="sol1", password="Senha@123Teste")
        resp = self.client.post(
            reverse("chamados:criar"),
            {
                "titulo": "Mouse com defeito",
                "descricao": "Roda do mouse parou.",
                "categoria": "HARDWARE",
                "prioridade": "MEDIA",
                "laboratorio": self.lab.id,
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Chamado.objects.count(), 1)
        ch = Chamado.objects.first()
        self.assertEqual(ch.solicitante, self.solicitante)
        self.assertEqual(ch.status, Chamado.NOVO)
        self.assertEqual(HistoricoStatus.objects.filter(chamado=ch).count(), 1)

    def test_tecnico_nao_ve_chamado_de_outro_tecnico(self):
        chamado_outro = Chamado.objects.create(
            titulo="Não meu",
            descricao="x",
            categoria="OUTROS",
            prioridade="BAIXA",
            laboratorio=self.lab,
            solicitante=self.solicitante,
            tecnico=self.tecnico2,
            status=Chamado.EM_ANDAMENTO,
        )
        self.client.login(username="tec1", password="Senha@123Teste")
        resp = self.client.get(reverse("chamados:detalhe", args=[chamado_outro.pk]))
        self.assertEqual(resp.status_code, 403)
        resp_lista = self.client.get(reverse("chamados:lista"))
        self.assertNotContains(resp_lista, "Não meu")

    def test_mudanca_status_grava_historico(self):
        chamado = Chamado.objects.create(
            titulo="Trocar status",
            descricao="x",
            categoria="OUTROS",
            prioridade="BAIXA",
            laboratorio=self.lab,
            solicitante=self.solicitante,
            tecnico=self.tecnico,
            status=Chamado.EM_ANDAMENTO,
        )
        HistoricoStatus.objects.create(
            chamado=chamado, de_status="", para_status=Chamado.NOVO, autor=self.solicitante
        )
        self.client.login(username="tec1", password="Senha@123Teste")
        resp = self.client.post(
            reverse("chamados:detalhe", args=[chamado.pk]),
            {"acao": "mudar_status", "status": Chamado.CONCLUIDO},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        chamado.refresh_from_db()
        self.assertEqual(chamado.status, Chamado.CONCLUIDO)
        self.assertIsNotNone(chamado.concluido_em)
        self.assertTrue(
            HistoricoStatus.objects.filter(
                chamado=chamado,
                de_status=Chamado.EM_ANDAMENTO,
                para_status=Chamado.CONCLUIDO,
            ).exists()
        )
