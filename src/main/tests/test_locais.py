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
class TesteLocais(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with self.app.session_transaction() as session:
            session['token'] = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

    def tearDown(self):
        with self.app.session_transaction() as session:
            session.pop('token', None)

    
    def test_retorna_as_informacoes_das_regioes_e_unidades(self):
        response = self.app.get(
            '/cp/locais'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
    unittest.main()