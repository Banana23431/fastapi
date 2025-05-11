from datetime import datetime
from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Название жанра не может быть пустым')
        return v

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int
    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    year: Optional[int]
    duration: Optional[int]
    rating: Optional[float]
    description: Optional[str]
    genre_ids: List[int] = []

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Название фильма не может быть пустым')
        return v

    @validator('rating')
    def rating_range(cls, v):
        if v is not None and not (0 <= v <= 10):
            raise ValueError('Рейтинг должен быть в диапазоне 0-10')
        return v

    @validator('year')
    def year_valid(cls, v):
        if v is not None and v < 1888:  # первый кинофильм
            raise ValueError('Некорректный год')
        return v

    @validator('duration')
    def duration_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Длительность должна быть положительной')
        return v

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int
    poster_url: Optional[str]
    date_added: datetime
    genres: List[GenreRead] = []

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True