from sqlalchemy.orm import Session
from .models import TeamContact


class TeamContactService:
    @staticmethod
    def list(db: Session):
        return db.query(TeamContact).all()

    @staticmethod
    def create(db: Session, team_contact: TeamContact):
        db.add(team_contact)
        db.commit()
        db.refresh(team_contact)
        return team_contact

    @staticmethod
    def update(db: Session, team_contact: TeamContact):
        db.commit()
        return team_contact

    @staticmethod
    def delete(db: Session, team_contact: TeamContact):
        db.delete(team_contact)
        db.commit()
