from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    genre_ids: List[int] = Field(default_factory=list)
    duration: Optional[int] = None
    rating: Optional[float] = None
    description: Optional[str] = None

    @validator('rating')
    def rating_range(cls, v):
        if v is not None and not (0 <= v <= 10):
            raise ValueError('Рейтинг должен быть в диапазоне 0-10')
        return v

class MovieCreate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int
    poster_url: Optional[HttpUrl]
    created_at: str
    genres: List[GenreRead] = []

    class Config:
        orm_mode = True
