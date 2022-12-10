from loguru import logger

import sqlite3
import json

from models.Film import Film


class Database:
    def __init__(self):
        self.connection = sqlite3.Connection("cimber_movies.db", timeout=10)
        self.cursor = self.connection.cursor()

        try:
            with self.connection:
                self.cursor.execute("""CREATE TABLE Film (
                    id INTEGER PRIMARY KEY,
                    name TEXT  UNIQUE NOT NULL,
                    year INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    countries  JSON NOT NULL,
                    duration  TEXT NOT NULL,
                    genres JSON NOT NULL,
                    poster  TEXT NOT NULL,
                    language INTEGER,
                    players JSON NOT NULL
                );""")
        except:
            pass

    def start(self):
        with open("cimber_temp.json", "r") as f:
            films = json.load(f)

        for film in films:
            self.add_film(Film.from_json(film))

    def add_film(self, film: Film) -> bool:
        try:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO Film (name, year, countries, duration, description, poster, players, language, genres) VALUES (?,?,?,?,?,?,?,?,?);",
                    (film.name, film.year, json.dumps(film.countries, ensure_ascii=False), film.duration, film.description, film.poster,
                     json.dumps(film.players, ensure_ascii=False), film.language.value, json.dumps(film.genres, ensure_ascii=False)))

                return True
        except Exception as e:
            if "UNIQUE" not in str(e):
                logger.error(str(e))
            elif "UNIQUE" in str(e):
                with self.connection:
                    exist_film = Film.from_sql(self.cursor.execute("SELECT * FROM Film WHERE name=?", (film.name,)).fetchone())

                    if not any(item in film.players for item in exist_film.players):
                        exist_film.players.extend(film.players)

                    if film != exist_film:
                        self.cursor.execute("UPDATE Film SET players=? WHERE name=?", (json.dumps(exist_film.players), exist_film.name))
                return True
        return False
