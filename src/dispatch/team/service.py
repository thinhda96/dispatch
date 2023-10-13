from sqlalchemy.orm import Session
from .models import TeamContact


class TeamContactService:
    @staticmethod
    def get(db_session: Session, id: int):
        return db_session.query(TeamContact).filter(TeamContact.id == id).first()

    @staticmethod
    def create(db_session: Session, **kwargs):
        team_contact = TeamContact(**kwargs)
        db_session.add(team_contact)
        db_session.commit()
        return team_contact

    @staticmethod
    def update(db_session: Session, team_contact: TeamContact, **kwargs):
        team_contact.update(**kwargs)
        db_session.commit()
        return team_contact

    @staticmethod
    def delete(db_session: Session, id: int):
        team_contact = TeamContactService.get(db_session, id)
        db_session.delete(team_contact)
        db_session.commit()
