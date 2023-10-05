from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dispatch.database.core import get_db
from .models import TeamContact
from .service import TeamContactService


router = APIRouter()


@router.get('/team_contacts')
def get_team_contacts(db: Session = Depends(get_db)):
    return TeamContactService.list(db)


@router.post('/team_contacts')
def create_team_contact(team_contact: TeamContact, db: Session = Depends(get_db)):
    return TeamContactService.create(db, team_contact)


@router.put('/team_contacts/{team_contact_id}')
def update_team_contact(team_contact_id: int, team_contact_in: TeamContact, db: Session = Depends(get_db)):
    team_contact = TeamContactService.get(db, team_contact_id)
    if not team_contact:
        raise HTTPException(status_code=404, detail='TeamContact not found')
    return TeamContactService.update(db, team_contact, team_contact_in)


@router.delete('/team_contacts/{team_contact_id}')
def delete_team_contact(team_contact_id: int, db: Session = Depends(get_db)):
    team_contact = TeamContactService.get(db, team_contact_id)
    if not team_contact:
        raise HTTPException(status_code=404, detail='TeamContact not found')
    TeamContactService.delete(db, team_contact)
    return {'detail': 'TeamContact deleted'}
