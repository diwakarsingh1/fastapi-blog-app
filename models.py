from sqlalchemy import String, Column, ForeignKey, PrimaryKeyConstraint, Integer, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Create_Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("Create_User", back_populates="blogs")

class Create_User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    
    blogs = relationship("Create_Blog", back_populates="creator")
