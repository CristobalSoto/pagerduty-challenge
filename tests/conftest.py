import pytest
from app import create_app
from config import TestingConfig
from app.models import db

@pytest.fixture(scope='module')
def test_client():
    """Set up the Flask test client and in-memory database."""
    app = create_app(TestingConfig)  # Use testing configuration with in-memory SQLite

    with app.test_client() as testing_client:
        with app.app_context():
            # Set up the in-memory test database
            db.create_all()
            yield testing_client  # This is where the test happens
            # Tear down the in-memory test database after testing
            db.drop_all()
