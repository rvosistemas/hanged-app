# Importa la clase Entity y otras dependencias necesarias
from ....application.domain.models.Entity import Entity, StatusEnum


def test_entity_creation():
    entity = Entity(
        id=1,
        status=StatusEnum.ACTIVE,
        created_at="2023-09-01 00:00:00",
        updated_at="2023-09-10 00:00:00",
        created_by="user1",
        updated_by="user1",
    )

    # Verifica que los atributos se inicializaron correctamente
    assert entity.id == 1
    assert entity.status == StatusEnum.ACTIVE
    assert entity.created_at == "2023-09-01 00:00:00"
    assert entity.updated_at == "2023-09-10 00:00:00"
    assert entity.created_by == "user1"
    assert entity.updated_by == "user1"
