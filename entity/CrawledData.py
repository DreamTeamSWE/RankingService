from typing import List

from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend
from entity.Image import Image


class CrawledData:
    def __init__(self, id_post: int = None, utente: str = None, data_post: str = None, caption: str = None,
                 restaurant: Restaurant = None) -> None:
        self.id_post = id_post
        self.utente = utente
        self.data_post = data_post
        self.caption = caption
        self.restaurant = restaurant
        self.list_image = None
        self.punt_emoji = None
        self.punt_foto = None
        self.score = None

    def set_score(self, score: ScoreComprehend):
        self.score = score

    def set_punt_foto(self, punt_foto: int):
        self.punt_foto = punt_foto

    def set_punt_emoji(self, punt_emoji: int):
        self.punt_emoji = punt_emoji

    def set_list_image(self, list_image: List[Image]):
        self.list_image = list_image

    def __str__(self):
        return "id_post: " + str(self.id_post) + "\n" + \
               "utente: " + str(self.utente) + "\n" + \
               "data_post: " + str(self.data_post) + "\n" + \
               "caption: " + str(self.caption) + "\n" + \
               "list_image: " + str(self.list_image) + "\n" + \
               "restaurant: " + str(self.restaurant) + "\n" + \
               "punt_emoji: " + str(self.punt_emoji) + "\n" + \
               "punt_foto: " + str(self.punt_foto) + "\n" + \
               "score: " + str(self.score)
