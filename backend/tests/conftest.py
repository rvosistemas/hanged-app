import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..application.domain.models.Entity import Base
from ..application.infrastructure.routers.authEndpoint import auth_bp
from ..application.infrastructure.routers.userEndpoint import user_bp


# @pytest.fixture
# def app():
#     app = Flask(__name__)
#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
#     app.register_blueprint(auth_bp, url_prefix="/api/auth")
#     app.register_blueprint(user_bp, url_prefix="/api/users")
#     yield app


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


# @pytest.fixture
# def client(app):
#     with app.test_client() as c:
#         yield c
