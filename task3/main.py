from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from models import Base,  Movie, Genre
from PYD.schemes import MovieCreate, MovieRead, GenreCreate, GenreRead
from database import SessionLocal,engine
from typing import List
import os
import uuid
import shutil

app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

POSTER_DIR = "posters"
os.makedirs(POSTER_DIR, exist_ok=True)


def save_image(file: UploadFile):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Недопустимый тип файла. Только JPEG и PNG.")

    filename = f"{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(POSTER_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return f"/{file_path}"


@app.get("/genres", response_model=List[GenreRead])
def read_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()

@app.post("/genres", response_model=GenreRead)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = Genre(name=genre.name, description=genre.description)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@app.get("/movies", response_model=List[MovieRead])
def read_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieRead)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie

@app.post("/movies", response_model=MovieRead)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(
        title=movie.title,
        year=movie.year,
        duration=movie.duration,
        rating=movie.rating,
        description=movie.description
    )

    genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()
    if len(genres) != len(movie.genre_ids):
        raise HTTPException(status_code=400, detail="Некорректные ID жанров")
    db_movie.genres = genres
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.put("/movies/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    db_movie.title = movie.title
    db_movie.year = movie.year
    db_movie.duration = movie.duration
    db_movie.rating = movie.rating
    db_movie.description = movie.description

    genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()
    if len(genres) != len(movie.genre_ids):
        raise HTTPException(status_code=400, detail="Некорректные ID жанров")
    db_movie.genres = genres
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    db.delete(db_movie)
    db.commit()
    return {"detail": "Фильм удален"}

@app.put("/movies/{movie_id}/image")
def upload_poster(movie_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")

    image_path = save_image(file)
    db_movie.poster_url = image_path
    db.commit()
    db.refresh(db_movie)
    return {"poster_url": image_path}