import unittest
import requests
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../python/'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
sys.argv.append('-t')
from webapp import app
import json, jwt, datetime

class TesteAgentes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        token = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        self.headers = {'token': token}

    def tearDown(self):
        self.headers = {'token': ''}


    def test_retorna_informacoes_de_todos_os_agentes(self):
        response = self.app.get(
            '/cp/agentes', 
            headers = self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_retorna_informacoes_de_um_agente(self):
        response = self.app.get(
            '/cp/agentes/1', 
            headers = self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    # def test_atualiza_informacoes_de_um_agente(self):
    #     response = self.app.put(
    #         'cp/agentes/1', 
    #         headers = self.headers, 
    #         data = json.dumps({
    #             "matricula": "", 
    #             "hora": "25:00", 
    #             "id_unidade": "", 
    #             "nome": "", 
    #             "sobrenome": "", 
    #             "email": "", 
    #             "cpf": "32132132121", 
    #             "senha": "", 
    #             "rg": "", 
    #             "dt_nascimento": "", 
    #             "genero": "", 
    #             "telefone": "", 
    #             "local_trabalho": "", 
    #             "cargo": "",
    #             "lattes": "", 
    #             "facebook": "facebook.com/agente3", 
    #             "linkedin": "", 
    #             "twitter": ""
    #         }), 
    #         follow_redirects = True, 
    #         content_type = "application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('sucesso', str(response.data))

    def test_cadastro_de_um_agente(self):
        response = self.app.post(
            '/cp/agentes', 
            headers = self.headers, 
            data = json.dumps({
                "id_parceiro": 2, 
                "hora": "30:00", 
                "matricula": 123123123, 
                "id_unidade": 1
            }), 
            follow_redirects = True, 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_exclui_um_agente(self):
        response = self.app.delete(
            'cp/agentes/2', 
            headers = self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_retorna_as_atividades_pendentes_de_um_agente(self):
        token = jwt.encode({'id_geral': 3, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        self.headers = {'token': token}
        
        response = self.app.get(
            '/cp/agentes/atividades', 
            headers = self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

    def test_retorno_de_uma_atividades_do_agente(self):
        token = jwt.encode({'id_geral': 3, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        self.headers = {'token': token}

        response = self.app.get(
            '/cp/agentes/atividades/1',
            headers = self.headers, 
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

    def test_atualizar_atividade(self):
        token = jwt.encode({'id_geral': 3, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        self.headers = {'token': token}
        
        response = self.app.put(
            '/cp/agentes/atividades/1',
            headers = self.headers, 
            data = json.dumps({
                "eixo": 1
            }),
            follow_redirects=True, 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

if __name__ == '__main__':
    unittest.main()