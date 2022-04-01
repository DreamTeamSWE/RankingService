from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend


class CrawledData:
    def __init__(self, id_post: int = None, id_restaurant: int = None, punt_emoji: int = None,
                 restaurant: Restaurant = None) -> None:
        self.id_post = id_post
        self.id_restaurant = id_restaurant
        self.punt_emoji = punt_emoji
        self.restaurant = restaurant
        self.score = None

    def set_point(self, score: ScoreComprehend):
        self.score = score
