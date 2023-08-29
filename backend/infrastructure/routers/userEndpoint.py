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


@user_bp.route("/users", methods=["GET"])
def get_users():
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return jsonify({"message": "Authorization header missing"}), 401

    token = auth_header.split(" ")[1]  # Obtén el token de Authorization header

    try:
        username = verify_token(token)
    except JWTError:
        return jsonify({"message": "Invalid token"}), 401

    users = user_service.get_all_users()
    serialized_users = [UserSerializer(user).to_dict() for user in users]
    return jsonify(serialized_users), 200
