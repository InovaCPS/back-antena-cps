# import unittest
# import requests
# import sys, os
# testdir = os.path.dirname(__file__)
# srcdir = '../python/'
# sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
# sys.argv.append('-t')
# from webapp import app
# import json, jwt, datetime

# # Fluxo
# # 1 - Diretor sobe a lista de presença de uma palestra
# # 2 - Parceiro que compareceu à palestra avalia a palestra
# # 3 - O mesmo parceiro retira o certificado
# # 4 - Diretor avalia o palestrante
# # 5 - Palestrante avalia a unidade

# class TesteFluxo2(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()

#     def tearDown(self):
#         with self.app.session_transaction() as session:
#             session.pop('token', None)

#     def test_1_sobe_lista_de_presenca(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.put(
#             '/cp/evento/4/inscritos/presenca', 
#             data = json.dumps({
#                 "lista":[
#                     {    
#                         "id_parceiro": "1", 
#                         "presenca": True
#                     },
#                     {    
#                         "id_parceiro": "6", 
#                         "presenca": True
#                     }
#                 ]
#             }), 
#             follow_redirects = True, 
#             content_type = "application/json"
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.content_type, 'application/json')

#     def test_2_avalia_evento(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 6, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.post(
#             '/cp/evento/4/avaliar', 
#             data = json.dumps({
#                 "nota": 4.5, 
#                 "comentario": "Excelente", 
#                 "identificar": True
#             }), 
#             follow_redirects=True, 
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('sucesso', str(response.data))

#     def test_3_retorna_o_certificado_de_um_evento_em_pdf(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 6, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.get(
#             '/cp/evento/4/certificado'
#         )
        
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.content_type, 'application/pdf')

#     def test_4_diretor_avalia_palestrante(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.post(
#             '/cp/evento/4/palestrante/1/avaliar', 
#             data = json.dumps({
#                 "nota": 5, 
#                 "comentario": "Excelente", 
#                 "identificar": True
#             }), 
#             follow_redirects=True, 
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('sucesso', str(response.data))

#     def test_5_palestrante_avalia_unidade(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.post(
#             '/cp/evento/4/unidade/avaliar', 
#             data = json.dumps({
#                 "nota": 4, 
#                 "comentario": "Excelente", 
#                 "identificar": True
#             }), 
#             follow_redirects=True, 
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('sucesso', str(response.data))