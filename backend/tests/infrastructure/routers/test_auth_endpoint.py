# import json
# from datetime import datetime
# from flask import url_for

# from ....application.domain.models.Enums import RoleEnum, StatusEnum


# def test_register_route(client, app):
#     # Prueba un registro válido
#     data = {
#         "username": "test_user",
#         "password": "password123",
#         "role": RoleEnum.ADMIN.value,
#         "status": StatusEnum.ACTIVE.value,
#         "created_at": datetime.now(),
#         "updated_at": datetime.now(),
#         "created_by": "test_user",
#         "updated_by": "test_user",
#     }

#     with app.app_context():
#         response = client.post(url_for("auth_bp.register"), json=data)
#         print("#" * 20, "response data: ", response.data)

#         decoded_data = response.data.decode("utf-8")
#         print("#" * 20, "decoded_data: ", decoded_data)

#     assert response.status_code == 201
#     data = json.loads(response.data)
#     assert "user" in data
#     assert "message" in data
#     assert data["message"] == "User registered successfully!"

#     # Prueba un registro con contraseña no coincidente
#     data = {"username": "test_user_2", "password": "password123", "password_confirm": "password456"}
#     response = client.post(url_for("auth_bp.register"), json=data)
#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert "message" in data
#     assert data["message"] == "Passwords do not match."

#     # Prueba un registro con un usuario que ya existe
#     data = {"username": "test_user", "password": "password123", "password_confirm": "password123"}
#     response = client.post(url_for("auth_bp.register"), json=data)
#     assert response.status_code == 409
#     data = json.loads(response.data)
#     assert "message" in data
#     assert data["message"] == "User already exists."


# def test_login_route(client):
#     # Prueba un inicio de sesión válido
#     data = {"username": "test_user", "password": "password123"}
#     response = client.post(url_for("auth_bp.login"), json=data)
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert "access_token" in data
#     assert "user" in data
#     assert "token_type" in data
#     assert "message" in data
#     assert data["message"] == "User logged in successfully"

#     # Prueba un inicio de sesión inválido (contraseña incorrecta)
#     data = {"username": "test_user", "password": "wrong_password"}
#     response = client.post(url_for("auth_bp.login"), json=data)
#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert "message" in data
#     assert data["message"] == "invalid credentials."
