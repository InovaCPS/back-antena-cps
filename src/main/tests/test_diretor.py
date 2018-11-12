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
class TesteDiretor(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

    def tearDown(self):
        with self.app.session_transaction() as session:
            session.pop('token', None)


    def test_retorna_informacoes_de_todos_os_diretores(self):
        response = self.app.get(
            '/cp/diretores'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_retorna_informacoes_de_um_diretor(self):
        response = self.app.get(
            '/cp/diretores/1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_cadastra_um_diretor(self):
        response = self.app.post(
            '/cp/diretores', 
            data = json.dumps({
                "id_unidade": "1", 
                "id_parceiro": "2"
            }), 
            follow_redirects=True, 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_exclui_um_diretor(self):
        response = self.app.delete(
            '/cp/diretores/2'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_retorna_atividades_de_um_diretor(self):
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        response = self.app.get(
            '/cp/diretores/atividades'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Mensagem', str(response.data))

    def test_retorna_informacoes_de_uma_atividade_diretor(self):
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        response = self.app.get(
            '/cp/diretores/atividades/2'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Mensagem', str(response.data))
        self.assertEqual(response.content_type, 'application/json')


    def test_autoriza_evento_diretor(self):
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        response = self.app.put(
            '/cp/diretores/atividades/2', 
            data = json.dumps({
                "resposta": True, 
                "capacidade": 30
            }), 
            follow_redirects=True, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Resposta cadastrada', str(response.data))

    def test_retorna_lista_de_alunos_da_unidade_diretor(self):
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        response = self.app.get(
            '/cp/diretores/alunos'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Mensagem', str(response.data))
        self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
    unittest.main()