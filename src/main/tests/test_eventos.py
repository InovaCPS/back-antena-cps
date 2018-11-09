import unittest
import requests
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../python/'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
sys.argv.append('-t')
from webapp import app
import json, jwt, datetime

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
        self.assertIn('nenhum evento', str(response.data))

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

# INCOMPLETO

if __name__ == '__main__':
    unittest.main()