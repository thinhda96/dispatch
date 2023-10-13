import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from dispatch.main import app
from dispatch.database.core import get_db
from dispatch.team.models import TeamContact
from dispatch.team.service import TeamContactService


def test_get_team_contact(db_session: Session):
    team_contact = TeamContactService.create(db_session, name='Test', email='test@example.com')
    client = TestClient(app)
    response = client.get(f'/team/{team_contact.id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Test'


def test_create_team_contact(db_session: Session):
    client = TestClient(app)
    response = client.post('/team/', json={'name': 'Test', 'email': 'test@example.com'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Test'


def test_update_team_contact(db_session: Session):
    team_contact = TeamContactService.create(db_session, name='Test', email='test@example.com')
    client = TestClient(app)
    response = client.put(f'/team/{team_contact.id}', json={'name': 'Updated'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated'


def test_delete_team_contact(db_session: Session):
    team_contact = TeamContactService.create(db_session, name='Test', email='test@example.com')
    client = TestClient(app)
    response = client.delete(f'/team/{team_contact.id}')
    assert response.status_code == 200
    assert response.json() == {'ok': True}
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from dispatch.main import app
from dispatch.database.core import get_db
from dispatch.team.models import TeamContact
from dispatch.team.service import TeamContactService


def test_get_team_contact(db_session: Session):
    team_contact = TeamContactService.create(db_session, name='Test', email='test@example.com')
    client = TestClient(app)
    response = client.get(f'/team/{team_contact.id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Test'


def test_create_team_contact(db_session: Session):
    client = TestClient(app)
    response = client.post('/team/', json={'name': 'Test', 'email': 'test@example.com'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Test'


def test_update_team_contact(db_session: Session):
    team_contact = TeamContactService.create(db_session, name='Test', email='test@example.com')
    client = TestClient(app)
    response = client.put(f'/team/{team_contact.id}', json={'name': 'Updated'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated'


def test_delete_team_contact(db_session: Session):
    team_contact = TeamContactService.create(db_session, name='Test', email='test@example.com')
    client = TestClient(app)
    response = client.delete(f'/team/{team_contact.id}')
    assert response.status_code == 200
    assert response.json() == {'ok': True}
