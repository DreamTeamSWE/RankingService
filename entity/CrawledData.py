from typing import List

from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend


class CrawledData:
    def __init__(self, id_post: int = None, utente: str = None, data_post: str = None, caption: str = None,
                 list_image: List[str] = None,
                 restaurant: Restaurant = None) -> None:
        self.id_post = id_post
        self.utente = utente
        self.data_post = data_post
        self.caption = caption
        self.list_image = list_image
        self.restaurant = restaurant
        self.punt_emoji = None
        self.score = None
        self.punt_foto = None

    def set_point(self, score: ScoreComprehend):
        self.score = score

    def set_punt_foto(self, punt_foto: int):
        self.punt_foto = punt_foto

    def set_punt_emoji(self, punt_emoji: int):
        self.punt_emoji = punt_emoji

    def __str__(self):
        return "id_post: " + str(
            self.id_post) + " utente: " + self.utente + " caption: " + self.caption + " list_image: " + str(
            self.list_image) + " restaurant: " + str(self.restaurant) + " punt_emoji: " + str(
            self.punt_emoji) + " score: " + str(
            self.score) + " punt_foto: " + str(self.punt_foto)
