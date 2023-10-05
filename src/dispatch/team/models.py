from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType
from dispatch.database.core import Base


class TeamContact(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    notes = Column(String)
    incidents = relationship('Incident', backref='team_contact', lazy=True)
    search_vector = Column(TSVectorType('name'))
