from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dispatch.database.core import get_db
from .models import TeamContact
from .service import TeamContactService


router = APIRouter()


@router.get('/{id}', response_model=TeamContact)
def get_team_contact(id: int, db_session: Session = Depends(get_db)):
    team_contact = TeamContactService.get(db_session, id)
    if not team_contact:
        raise HTTPException(status_code=404, detail='TeamContact not found')
    return team_contact


@router.post('/', response_model=TeamContact)
def create_team_contact(team_contact: TeamContact, db_session: Session = Depends(get_db)):
    return TeamContactService.create(db_session, **team_contact.dict())


@router.put('/{id}', response_model=TeamContact)
def update_team_contact(id: int, team_contact: TeamContact, db_session: Session = Depends(get_db)):
    db_team_contact = TeamContactService.get(db_session, id)
    if not db_team_contact:
        raise HTTPException(status_code=404, detail='TeamContact not found')
    return TeamContactService.update(db_session, db_team_contact, **team_contact.dict())


@router.delete('/{id}')
def delete_team_contact(id: int, db_session: Session = Depends(get_db)):
    team_contact = TeamContactService.get(db_session, id)
    if not team_contact:
        raise HTTPException(status_code=404, detail='TeamContact not found')
    TeamContactService.delete(db_session, id)
    return {'ok': True}
