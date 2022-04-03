from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend


class CrawledData:
    def __init__(self, id_post: int = None,
                 restaurant: Restaurant = None) -> None:
        self.id_post = id_post
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
