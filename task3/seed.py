from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    genre1 = models.Genre(name="Драма", description="Драматические фильмы")
    genre2 = models.Genre(name="Комедия", description="Комедийные фильмы")
    db.add_all([genre1, genre2])
    db.commit()


    from datetime import datetime
    movie1 = models.Movie(
        title="Интерстеллар",
        year=2014,
        duration=169,
        rating=8.6,
        description="Фантастический фильм о космосе",
        date_added=datetime.utcnow(),
        genres=[genre1]
    )

    movie2 = models.Movie(
        title="Маска",
        year=1994,
        duration=101,
        rating=7.3,
        description="Комедия с Джимом Керри",
        date_added=datetime.utcnow(),
        genres=[genre2]
    )

    db.add_all([movie1, movie2])
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()