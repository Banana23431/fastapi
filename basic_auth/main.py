from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from datetime import datetime
from uuid import uuid4
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Security
from database import engine, get_db
import models
from PYD.schemes import *
from utils import save_poster

models.Base.metadata.create_all(bind=engine)


security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    return user

app = FastAPI()

@app.get("/movies", response_model=List[MovieRead])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    return movies


@app.get("/movies/{movie_id}", response_model=MovieRead)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie


@app.post("/movies", response_model=MovieRead)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = models.Movie(
        title=movie.title,
        year=movie.year,
        duration=movie.duration,
        rating=movie.rating,
        description=movie.description,
        date_added=datetime.utcnow()
    )


    if movie.genre_ids:
        genres = db.query(models.Genre).filter(models.Genre.id.in_(movie.genre_ids)).all()
        db_movie.genres = genres
        

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
pass

@app.put("/movies/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    for var, value in vars(movie).items():
        if value is not None:
            setattr(db_movie, var, value)


    if movie.genre_ids:
        genres = db.query(models.Genre).filter(models.Genre.id.in_(movie.genre_ids)).all()
        db_movie.genres = genres
        

    db.commit()
    db.refresh(db_movie)
    return db_movie
pass

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    db.delete(movie)
    db.commit()
    return {"detail": "Фильм удален"}
pass


@app.put("/movies/{movie_id}/image")
def update_movie_image(movie_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Недопустимый тип файла. Только JPEG и PNG.")


    contents = file.file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл слишком большой (максимум 5MB).")
    file.file.seek(0)


    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    

    filename = save_poster(file.filename, contents)


    movie.poster_url = filename
    db.commit()
    db.refresh(movie)
    return {"poster_url": filename}
pass


@app.get("/genres", response_model=List[GenreRead])
def get_genres(db: Session = Depends(get_db)):
    return db.query(models.Genre).all()

@app.post("/genres", response_model=GenreRead)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    existing_genre = db.query(models.Genre).filter(models.Genre.name == genre.name).first()
    if existing_genre:
        raise HTTPException(status_code=400, detail="Жанр с таким именем уже существует")
    db_genre = models.Genre(
        name=genre.name,
        description=genre.description
    )
    
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre
pass

@app.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Имя пользователя занято")
    
    
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
pass