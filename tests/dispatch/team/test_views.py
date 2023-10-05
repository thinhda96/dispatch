import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from dispatch.database.core import Base
from dispatch.team.models import TeamContact
from dispatch.team.service import TeamContactService
from main import app

client = TestClient(app)


def test_get_team_contacts(db: Session):
    team_contact = TeamContact(name='Test', email='test@example.com', notes='Test notes')
    TeamContactService.create(db, team_contact)
    response = client.get('/team_contacts')
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Test', 'email': 'test@example.com', 'notes': 'Test notes'}]


def test_create_team_contact(db: Session):
    response = client.post('/team_contacts', json={'name': 'Test', 'email': 'test@example.com', 'notes': 'Test notes'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Test', 'email': 'test@example.com', 'notes': 'Test notes'}


def test_update_team_contact(db: Session):
    team_contact = TeamContact(name='Test', email='test@example.com', notes='Test notes')
    TeamContactService.create(db, team_contact)
    response = client.put('/team_contacts/1', json={'name': 'Updated', 'email': 'updated@example.com', 'notes': 'Updated notes'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Updated', 'email': 'updated@example.com', 'notes': 'Updated notes'}


def test_delete_team_contact(db: Session):
    team_contact = TeamContact(name='Test', email='test@example.com', notes='Test notes')
    TeamContactService.create(db, team_contact)
    response = client.delete('/team_contacts/1')
    assert response.status_code == 200
    assert response.json() == {'message': 'TeamContact deleted successfully'}
