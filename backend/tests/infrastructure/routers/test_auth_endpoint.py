# import json
# import pytest
# from flask import Flask

# from ....application.domain.models.Entity import Base
# from ....application.infrastructure.routers.authEndpoint import auth_bp

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


# @pytest.fixture
# def app():
#     app = Flask(__name__)
#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Utiliza la base de datos en memoria
#     app.register_blueprint(auth_bp)
#     yield app


# @pytest.fixture
# def client2(app):
#     TEST_DATABASE_URL = "sqlite:///:memory:"

#     engine = create_engine(TEST_DATABASE_URL, echo=True)
#     engine.dispose()
#     engine = create_engine(TEST_DATABASE_URL, echo=True)
#     Session = sessionmaker(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     session = Session()
#     with app.test_client(session) as client:
#         yield client


# def test_home_endpoint(client2):
#     response = client2.get("/")
#     data = json.loads(response.get_data(as_text=True))
#     print("#" * 20, "data: ", data)
#     assert response.status_code == 200
#     assert data["message"] == "Auth endpoint."


# def test_register_endpoint(client2):
#     new_user_data = {"username": "new_user", "password": "password123", "password_confirm": "password123"}
#     response = client2.post("/register", json=new_user_data)
#     print("#" * 20, "response: ", response)
#     print("#" * 20, "response data: ", response.data)
#     data = json.loads(response.get_data(as_text=True))
#     assert response.status_code == 201
#     assert data["message"] == "User registered successfully!"

#     # Verificar que el usuario fue creado correctamente en la base de datos, si es aplicable


# def test_login_endpoint(client):
#     user_data = {"username": "existing_user", "password": "password123"}
#     response = client.post("/login", json=user_data)
#     data = json.loads(response.get_data(as_text=True))
#     assert response.status_code == 200
#     assert data["status"] == "success"
#     assert "access_token" in data
#     assert data["message"] == "User logged in successfully"


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
