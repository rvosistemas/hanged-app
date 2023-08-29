# app.py
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from infrastructure.core.settings import Settings

from domain.models.Entity import Base

from infrastructure.core.database import engine
from infrastructure.routers.authEndpoint import auth_bp
from infrastructure.routers.userEndpoint import user_bp

load_dotenv()

settings = Settings()

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/users")

app.route("/")(lambda: "Hello, world! This is the home page.")

if __name__ == "__main__":
    app.run(debug=settings.DEBUG)
