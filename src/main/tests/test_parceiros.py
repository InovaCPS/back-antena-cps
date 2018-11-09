import unittest
import requests
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../python/'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
sys.argv.append('-t')
from webapp import app
import json, jwt, datetime

class TesteParceiros(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

    def tearDown(self):
        with self.app.session_transaction() as session:
            session.pop('token', None)


    def test_retorno_das_informacoes_de_todos_os_parceiros(self):
        response = self.app.get(
            '/cp/parceiro'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('application/json', response.content_type)

    def test_retorno_das_informacoes_de_um_parceiro(self):
        response = self.app.get(
            '/cp/parceiro/1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('encontrado', str(response.data))

    def test_cadastro_de_parceiro(self):
        response = self.app.post(
            '/cp/parceiro',
            data = json.dumps({
                "nome": "Irmão", 
                "sobrenome": "do Jorel", 
                "email": "irmaodojorel@email.com", 
                "senha": "1234"
            }),
            follow_redirects=True, 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_atualiza_informacoes_de_um_parceiro(self):
        response = self.app.put(
            '/cp/parceiro/2', 
            data = json.dumps({
                "nome": "João", 
                "sobrenome": "da Silva", 
                "email": "joao@email.com", 
                "cpf": "32132132121", 
                "senha": "1234", 
                "rg": "", 
                "dt_nascimento": "", 
                "genero": "", 
                "telefone": "12345678", 
                "local_trabalho": "", 
                "cargo": "",
                "lattes": "", 
                "facebook": "", 
                "linkedin": "", 
                "twitter": ""
            }), 
            follow_redirects=True, 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

    def test_exclui_um_parceiro(self):
        response = self.app.delete(
            '/cp/parceiro/7'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sucesso', str(response.data))

if __name__ == '__main__':
    unittest.main()