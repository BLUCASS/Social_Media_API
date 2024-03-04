from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///data.db')
Base = declarative_base()


class User(Base):
    """This table contains the user's information"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(30), nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(44), nullable=False)

class Posts(Base):
    """This tables contains the users posts"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, nullable=False)
    post = Column(String, nullable=False)

Base.metadata.create_all(engine)