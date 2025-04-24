from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

movie_genre_association = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    movies = relationship('Movie', secondary=movie_genre_association, back_populates='genres')

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    year = Column(Integer)
    duration = Column(Integer)
    rating = Column(Float)
    description = Column(Text)
    poster_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    genres = relationship('Genre', secondary=movie_genre_association, back_populates='movies')
