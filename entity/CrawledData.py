from typing import List

from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend


class CrawledData:
    def __init__(self, caption: str, image: List[str], restaurant: Restaurant):
        self.caption = caption
        self.image = image
        self.restaurant = restaurant
        self.score = None

    def set_point(self, score: ScoreComprehend):
        self.score = score
