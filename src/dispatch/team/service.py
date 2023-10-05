from sqlalchemy.orm import Session
from .models import TeamContact


class TeamContactService:
    @staticmethod
    def list(db_session: Session):
        return db_session.query(TeamContact).all()

    @staticmethod
    def create(db_session: Session, team_contact: TeamContact):
        db_session.add(team_contact)
        db_session.commit()
        db_session.refresh(team_contact)
        return team_contact

    @staticmethod
    def update(db_session: Session, team_contact: TeamContact, team_contact_in: TeamContact):
        team_contact.update(team_contact_in.dict())
        db_session.commit()
        return team_contact

    @staticmethod
    def delete(db_session: Session, team_contact: TeamContact):
        db_session.delete(team_contact)
        db_session.commit()
