from loguru import logger

import json
from dataclasses import dataclass

from models.Language import Language


@dataclass
class Film:
    name: str
    year: int
    description: str
    countries: list
    duration: str
    genres: list
    poster: str
    language: Language
    players: list


    def from_sql(film: tuple):
        return Film(film[1], film[2], film[3],
                    json.loads(film[4]), film[5],
                    json.loads(film[6]), film[7],
                    film[8], json.loads(film[9]))

    def from_json(film: dict):
        try:
            return Film(film["name"], int(film["year"]), film["description"], film["countries"],
                        film["duration"], film["genres"], film["poster"], Language.Russian,
                        film["players"])
        except Exception as e:
            logger.error(str(e))