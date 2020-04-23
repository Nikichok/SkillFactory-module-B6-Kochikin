import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def add_album(album_data):
    """
    Осуществляет добавление альбомов новых исполнителей
    """
    session = connect_db()
    # формируем строку в таблицу Album
    new_album = Album(
        year=int(album_data["year"]),
        artist=album_data["artist"],
        genre=album_data["genre"],
        album=album_data["album"]
        )
    # добавляем строку в сессию
    session.add(new_album)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    return("Альбом {0} исполнителя {1} добавлен!".format(album_data["album"], album_data["artist"]))

def check_album(album_data):
    """
    Проверяет наличие альбома в базе
    """
    session = connect_db()
    # возвращаем наличие в базе по названию альбома и исполнителя
    return(session.query(Album).filter(Album.artist == album_data["artist"], Album.album == album_data["album"]).count())
       