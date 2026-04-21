import app.db.models
import pytest

from app.db.base import Base
from app.db.session import engine


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=engine)
    yield
