from flask import Blueprint, jsonify, request
from domain.serializers.userSerializers import UserSerializer
from jose import jwt, JWTError

from ..core.settings import Settings
from ..utils.passwordManager import PasswordManager

from domain.repositories.UserSqlRepository import UserSqlRepository
from domain.serializers.userSerializers import UserSerializer
from domain.services.UserService import UserService

from infrastructure.core.database import SessionLocal
from infrastructure.utils.token import verify_token

user_bp = Blueprint("user_bp", __name__)

settings = Settings()

user_repository = UserSqlRepository(SessionLocal())
user_service = UserService(user_repository)
password_manager = PasswordManager()


def get_authorization_token(request) -> str or tuple:
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return jsonify({"message": "Authorization header missing"}), 401

    token = auth_header.split(" ")[1]  # Obtén el token de Authorization header

    try:
        return verify_token(token)
    except JWTError:
        return jsonify({"message": "Invalid token"}), 401


@user_bp.route("/users", methods=["GET"])
def get_users():
    get_authorization_token(request)
    users = user_service.get_all_users()
    serialized_users = [UserSerializer(user).to_dict() for user in users]
    return jsonify(serialized_users), 200


@user_bp.route("/users", methods=["POST"])
def create_user():
    get_authorization_token(request)
    data = request.get_json()
    print("#" * 20, "data: ", data)
    user = user_service.create_user(data)
    serialized_user = UserSerializer(user).to_dict()
    return jsonify(serialized_user), 201
