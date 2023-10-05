import pytest
from sqlalchemy.orm import Session
from dispatch.database.core import Base
from dispatch.team.models import TeamContact
from dispatch.team.service import TeamContactService


def test_get_team_contacts(db: Session):
    team_contacts = TeamContactService.list(db)
    assert team_contacts is not None


def test_create_team_contact(db: Session):
    team_contact_in = TeamContact(name='Test', email='test@example.com', notes='Test notes')
    team_contact = TeamContactService.create(db, team_contact_in)
    assert team_contact.id is not None
    assert team_contact.name == 'Test'
    assert team_contact.email == 'test@example.com'
    assert team_contact.notes == 'Test notes'


def test_update_team_contact(db: Session):
    team_contact_in = TeamContact(name='Test', email='test@example.com', notes='Test notes')
    team_contact = TeamContactService.create(db, team_contact_in)
    team_contact_in2 = TeamContact(name='Test2', email='test2@example.com', notes='Test notes 2')
    team_contact2 = TeamContactService.update(db, team_contact, team_contact_in2)
    assert team_contact2.id == team_contact.id
    assert team_contact2.name == 'Test2'
    assert team_contact2.email == 'test2@example.com'
    assert team_contact2.notes == 'Test notes 2'


def test_delete_team_contact(db: Session):
    team_contact_in = TeamContact(name='Test', email='test@example.com', notes='Test notes')
    team_contact = TeamContactService.create(db, team_contact_in)
    TeamContactService.delete(db, team_contact)
    team_contact2 = TeamContactService.get(db, team_contact.id)
    assert team_contact2 is None
