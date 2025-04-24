from sqlalchemy.orm import Session
from models import Base, engine, Genre, Movie

def seed():
    db = Session(bind=engine)


    genre1 = Genre(name='Драма', description='Драматические фильмы')
    genre2 = Genre(name='Комедия', description='Веселые фильмы')
    db.add_all([genre1, genre2])
    db.commit()


    movie1 = Movie(
        title='Интерстеллар',
        year=2014,
        duration=169,
        rating=8.6,
        description='Научно-фантастический фильм о путешествии во времени и пространстве.',
        poster_url='http://example.com/posters/interstellar.jpg',
        genres=[genre1]
    )

    movie2 = Movie(
        title='Маска',
        year=1994,
        duration=104,
        rating=7.3,
        description='Комедийный фильм с Джимом Керри.',
        poster_url='http://example.com/posters/mask.jpg',
        genres=[genre2]
    )

    db.add_all([movie1, movie2])
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
