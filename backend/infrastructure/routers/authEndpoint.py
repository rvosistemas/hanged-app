from flask import Blueprint, jsonify, request

from ..core.settings import Settings
from ..utils.passwordManager import PasswordManager
from ..utils.token import create_access_token

from domain.models.Enums import RoleEnum, StatusEnum
from domain.repositories.UserSqlRepository import UserSqlRepository
from domain.serializers.userSerializers import UserSerializer
from domain.services.UserService import UserService

from infrastructure.core.database import SessionLocal

settings = Settings()

user_repository = UserSqlRepository(SessionLocal())
user_service = UserService(user_repository)
password_manager = PasswordManager()

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Auth endpoint."})


@auth_bp.route("/register", methods=["POST"])
def register() -> tuple:
    user_data = request.get_json()
    user = user_service.get_user_by_username(user_data["username"])
    if user:
        return jsonify({"message": "User already exists."}), 409
    if user_data["password"] != user_data["password_confirm"]:
        return jsonify({"message": "Passwords do not match."}), 400

    user_data["role"] = RoleEnum.FINAL_USER.value

    if (user_data["username"] == settings.ADMIN) and (user_data["password"] == settings.SECRET_KEY):
        user_data["role"] = RoleEnum.ADMIN.value

    user_data["password"] = password_manager.encrypt_password(user_data["password"])

    del user_data["password_confirm"]

    user_created = user_service.create_user(user_data)
    new_user = UserSerializer(user_created).to_dict()

    return jsonify({"user": new_user, "message": "User registered successfully!"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    user_data = request.get_json()
    user = user_service.get_user_by_username(user_data["username"])
    user = UserSerializer(user).to_dict()
    if (
        not user
        or user["status"] == StatusEnum.INACTIVE
        or not password_manager.verify_password(user_data["password"], user["password"])
    ):
        return jsonify({"message": "invalid credentials."}), 400
    access_token = create_access_token(username=user["username"])

    responseUser = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "status": user["status"],
    }

    return jsonify(
        {
            "status": "success",
            "user": responseUser,
            "access_token": access_token,
            "token_type": "bearer",
            "message": "User logged in successfully",
        }
    )
