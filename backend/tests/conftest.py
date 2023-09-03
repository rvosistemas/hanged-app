import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..application.domain.models.Entity import Base
from ..application.infrastructure.routers.authEndpoint import auth_bp
from ..application.infrastructure.routers.userEndpoint import user_bp


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    return app


@pytest.fixture
def db_session():
    TEST_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(TEST_DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def client(app):
    with app.test_client(db_session) as c:
        yield c
