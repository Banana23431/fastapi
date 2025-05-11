from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

movie_genre_association = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    movies = relationship('Movie', secondary=movie_genre_association, back_populates='genres')

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    year = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)  
    rating = Column(Float, nullable=True) 
    description = Column(Text, nullable=True)
    poster_url = Column(String(255), nullable=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    genres = relationship('Genre', secondary=movie_genre_association, back_populates='movies')