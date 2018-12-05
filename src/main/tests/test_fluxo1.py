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
# # 1 - Parceiro se cadastra na plataforma
# # 2 - Parceiro cadastra uma palestra
# # 3 - Agente avalia a palestra
# # 4 - Diretor da unidade autoriza a palestra
# # 5 - Parceiro se cadastra na palestra

# class TesteFluxo1(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#     def tearDown(self):
#         with self.app.session_transaction() as session:
#             session.pop('token', None)

#     def test_1_cadastro_de_parceiro(self):
#         response = self.app.post(
#             '/cp/parceiro',
#             data = json.dumps({
#                 "nome": "Irmão", 
#                 "sobrenome": "do Jorel", 
#                 "email": "irmaodojorel@email.com", 
#                 "senha": "1234"
#             }),
#             follow_redirects=True, 
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('sucesso', str(response.data))

#     def test_2_cadastro_de_evento(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 7, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.post(
#             '/cp/evento', 
#             data = json.dumps({
#                 "titulo": "como programar Orientado a Objeto", 
#                 "descricao": "será explicado como programar Orientado a Objeto", 
#                 "tipo": "curso", 
#                 "duracao": "60", 
#                 "banner": "o caminho do banner", 
#                 "eventos":[
#                     ["1", "2019-10-15", "14:00"], 
#                     ["1", "2019-10-16", "14:00"], 
#                     ["1", "2019-10-17", "14:00"]
#                 ], 
#                 "materiais":[
#                     ["caminho do material 1"], 
#                     ["caminho do material 2"]
#                 ]
#             }), 
#             follow_redirects = True, 
#             content_type = "application/json"
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Cadastrado com sucesso', str(response.data))

#     def test_3_agente_atribui_eixo_da_atividade(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 3, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
#         response = self.app.put(
#             '/cp/agentes/atividades/3',
#             data = json.dumps({
#                 "eixo": 1
#             }),
#             follow_redirects=True, 
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual('application/json', response.content_type)

#     def test_4_diretor_autoriza_evento(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 4, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
#         response = self.app.put(
#             '/cp/diretores/atividades/6', 
#             data = json.dumps({
#                 "resposta": True, 
#                 "capacidade": 30
#             }), 
#             follow_redirects=True, 
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Resposta cadastrada', str(response.data))

#     def test_5_cadastra_o_usuario_num_evento(self):
#         with self.app.session_transaction() as session:
#             session['token'] = jwt.encode({'id_geral': 6, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])

#         response = self.app.post(
#             '/cp/evento/6/inscrito'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('sucesso', str(response.data))

# if __name__ == '__main__':
#     unittest.main()