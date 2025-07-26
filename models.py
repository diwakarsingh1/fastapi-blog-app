from sqlalchemy import String, Column, ForeignKey, PrimaryKeyConstraint, Integer, Boolean
from database import Base

class Create_Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)

