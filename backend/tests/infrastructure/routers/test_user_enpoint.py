# import unittest
# from flask import Flask
# from ....application.infrastructure.routers.userEndpoint import user_bp


# class TestUserRoutes(unittest.TestCase):
#     def setUp(self):
#         self.app = Flask(__name__)
#         self.app.register_blueprint(user_bp)
#         self.client = self.app.test_client()

#     def test_get_users_route(self):
#         response = self.client.get("/all")
#         self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200

#     def test_get_user_route(self):
#         response = self.client.get("/one/1")  # Cambia el número según tu caso de prueba
#         self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200

#     def test_create_user_route(self):
#         # Aquí puedes enviar una solicitud POST simulada con datos de usuario
#         response = self.client.post("/create", json={"username": "testuser", "password": "password"})
#         self.assertEqual(response.status_code, 201)  # Verifica que el código de estado sea 201

#     def test_update_user_route(self):
#         # Aquí puedes enviar una solicitud PUT simulada con datos de usuario
#         response = self.client.put("/update/1", json={"username": "updateduser"})
#         self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200

#     def test_delete_user_route(self):
#         response = self.client.delete("/delete/1")  # Cambia el número según tu caso de prueba
#         self.assertEqual(response.status_code, 200)  # Verifica que el código de estado sea 200
