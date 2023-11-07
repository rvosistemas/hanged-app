from ....application.infrastructure.core.database import engine, SessionLocal
from ....application.infrastructure.core.settings import Settings

settings = Settings()


def test_database_config():
    # Verifica que el motor de la base de datos sea una instancia válida de SQLAlchemy
    assert engine is not None
    assert str(engine.url) == "sqlite:///./application/database/settings.DATABASE"

    # Intenta crear una sesión y verifica que sea una instancia válida
    session = SessionLocal()
    assert session is not None

    # Intenta cerrar la sesión sin errores
    session.close()


# Ejecuta el test
def test_database_config():
    # Verifica que el motor de la base de datos sea una instancia válida de SQLAlchemy
    assert engine is not None
    assert str(engine.url) == f"sqlite:///./application/database/{settings.DATABASE}"

    # Intenta crear una sesión y verifica que sea una instancia válida
    session = SessionLocal()
    assert session is not None

    # Intenta cerrar la sesión sin errores
    session.close()
