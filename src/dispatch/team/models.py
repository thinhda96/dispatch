from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType
from dispatch.database.core import Base
from dispatch.models import TimeStampMixin, ProjectMixin


class TeamContact(Base, TimeStampMixin, ProjectMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    notes = Column(String)
    incidents = relationship('Incident', backref='team_contact')
    search_vector = Column(TSVectorType('name'))
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType
from dispatch.database.core import Base
from dispatch.models import TimeStampMixin, ProjectMixin


class TeamContact(Base, TimeStampMixin, ProjectMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    notes = Column(String)
    incidents = relationship('Incident', backref='team_contact')
    search_vector = Column(TSVectorType('name'))
