from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

class AlbumError(Exception):
    """
    Используется для идентификации некорректных параметров Альбомов для добавления
    """
    pass
   

def make_russian(n):
    last_digit = n % 10
    last_two = n % 100
    if last_digit == 1 and last_two != 11:
        ending = "альбом"
    elif last_digit in [2, 3, 4] and not (last_two in [12, 13, 14]):
        ending = "альбома"
    else:
        ending = "альбомов"
    return str(n) + " " + ending

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        num_albums = len(album_names)
        str_albums = make_russian(num_albums)
        result = "У исполнителя {} {}:<br>".format(artist, str_albums)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def albums():
    album_data = {
        "year":request.forms.year,
        "artist":request.forms.artist,
        "genre":request.forms.genre,
        "album":request.forms.album
    }
    if not int(album_data["year"]) or int(album_data["year"]) > 2020:
        raise AlbumError("Некорректно указан год")
    elif not isinstance(album_data["artist"], str):
        raise AlbumError("Исполнитель указан некорректно (не является строковым)")
    elif not isinstance(album_data["genre"], str):
        raise AlbumError("Жанр указан некорректно (не является строковым)")
    elif not isinstance(album_data["album"], str):
        raise AlbumError("Альбом указан некорректно (не является строковым)")
    elif album.check_album(album_data):
        message = "Альбом {} исполнителя {} уже есть в базе".format(album_data["album"], album_data["artist"])
        result = HTTPError(409, message)
    else:
        result = album.add_album(album_data)
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)