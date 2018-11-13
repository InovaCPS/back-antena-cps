import unittest
import requests
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../python/'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
sys.argv.append('-t')
from webapp import app
import json, jwt, datetime

# COMPLETO
class TesteEventos(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

    def tearDown(self):
        with self.app.session_transaction() as session:
            session.pop('token', None)

    
    def test_retorno_das_informacoes_de_todos_os_eventos(self):
        response = self.app.get(
            '/cp/eventos'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

    def test_retorno_dos_eventos_que_o_usuario_esta_cadastrado(self):
        response = self.app.get(
            '/cp/meuseventos'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

    def test_retorno_das_informacoes_de_um_evento(self):
        response = self.app.get(
            '/cp/evento/1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

    def test_cadastro_de_evento(self):
        response = self.app.post(
            '/cp/evento', 
            data = json.dumps({
                "titulo": "como programar Orientado a Objeto", 
                "descricao": "será explicado como programar Orientado a Objeto", 
                "tipo": "curso", 
                "duracao": "60", 
                "banner": "o caminho do banner", 
                "eventos":[
                    ["1", "2018-10-15", "14:00"], 
                    ["1", "2018-10-16", "14:00"], 
                    ["1", "2018-10-17", "14:00"]
                ], 
                "materiais":[
                    ["caminho do material 1"], 
                    ["caminho do material 2"]
                ]
            }), 
            follow_redirects = True, 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cadastrado com sucesso', str(response.data))

    def test_atualizacao_de_evento(self):
        response = self.app.put(
            '/cp/evento/1', 
            data = json.dumps({
                "titulo": "como programar em python e flask", 
                "descricao": "será explicado como programar em python e flask", 
                "tipo": "curso", 
                "duracao": "40", 
                "banner": "o caminho do banner", 
                "eventos":[
                    ["1", "1", "2020-07-15", "17:00"], 
                    ["3", "1", "2020-07-16", "20:30"],
                    ["", "1", "2020-07-17", "19:30"]
                ], 
                "materiais":[
                    ["2", "novo caminho do material 2"],
                    ["", "caminho do material 3"]
                ], 
                "exclui_eventos": [
                    ["2"]
                ], 
                "exclui_materiais": [
                    ["1"]
                ]
            }), 
            follow_redirects = True, 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_retorna_lista_de_inscritos_de_um_evento_em_json(self):
        response = self.app.get(
            '/cp/evento/1/inscritos'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_retorna_lista_de_inscritos_de_um_evento_em_pdf(self):
        response = self.app.get(
            '/cp/evento/1/lista'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_cadastra_o_usuario_num_evento(self):
        response = self.app.post(
            '/cp/evento/5/inscrito'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_exclui_o_cadastro_de_um_usuario_num_evento(self):
        response = self.app.delete(
            '/cp/evento/5/inscrito'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_exclui_evento(self):
        response = self.app.delete(
            '/cp/evento/3'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_retorna_o_certificado_de_um_evento_em_pdf(self):
        response = self.app.get(
            '/cp/evento/1/certificado'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_sobe_lista_de_presenca(self):
        response = self.app.put(
            '/cp/evento/1/inscritos/presenca', 
            data = json.dumps({
                "lista":[
                    {    
                        "id_parceiro": "1", 
                        "presenca": True
                    },
                    {    
                        "id_parceiro": "6", 
                        "presenca": True
                    }
                ]
            }), 
            follow_redirects = True, 
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_avalia_evento(self):
        response = self.app.post(
            '/cp/evento/4/avaliar', 
            data = json.dumps({
                "nota": 4.5, 
                "comentario": "Excelente", 
                "identificar": True
            }), 
            follow_redirects=True, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_retorna_eventos_pendentes_para_avaliacao(self):
        response = self.app.get(
            '/cp/evento/avaliacao'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('"Mensagem":', str(response.data))

    def test_diretor_avalia_palestrante(self):
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        response = self.app.post(
            '/cp/evento/4/palestrante/1/avaliar', 
            data = json.dumps({
                "nota": 5, 
                "comentario": "Excelente", 
                "identificar": True
            }), 
            follow_redirects=True, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_palestrante_avalia_unidade(self):
        response = self.app.post(
            '/cp/evento/4/unidade/avaliar', 
            data = json.dumps({
                "nota": 4, 
                "comentario": "Excelente", 
                "identificar": True
            }), 
            follow_redirects=True, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

if __name__ == '__main__':
    unittest.main()