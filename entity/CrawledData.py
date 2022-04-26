from typing import List
from datetime import datetime

from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend
from entity.Image import Image


class CrawledData:
    def __init__(self, id_post: str = None, utente: str = None,
                 data_post: str = datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), caption: str = None,
                 restaurant: Restaurant = None, list_images: List[Image] = None) -> None:
        self.id_post = id_post
        self.utente = utente
        self.data_post = data_post
        self.caption = caption
        self.restaurant = restaurant
        self.list_images = list_images
        self.punt_emoji = None
        self.punt_foto = None
        self.punt_testo = None
        self.comprehend_score = None

    def set_punt_testo(self):
        if self.comprehend_score:
            self.punt_testo = self.comprehend_score.calculate_score()

    def calculate_and_set_punt_foto(self):
        if self.list_images:
            for image in self.list_images:
                score = image.calculate_score()
                if score is not None:
                    self.punt_foto = (self.punt_foto + score) if self.punt_foto is not None else score

    def set_punt_emoji(self, punt_emoji: float):
        self.punt_emoji = punt_emoji

    def set_comprehend_score(self, score: ScoreComprehend):
        self.comprehend_score = score

    def __str__(self):
        return "id_post: " + str(self.id_post) + "\n" + \
               "utente: " + str(self.utente) + "\n" + \
               "data_post: " + str(self.data_post) + "\n" + \
               "caption: " + str(self.caption) + "\n" + \
               "list_image: " + str(self.list_images) + "\n" + \
               "restaurant: " + str(self.restaurant) + "\n" + \
               "punt_emoji: " + str(self.punt_emoji) + "\n" + \
               "punt_foto: " + str(self.punt_foto) + "\n" + \
               "punt_testo: " + str(self.punt_testo)

    @staticmethod
    def parse_post_from_sqs(item_body: dict):
        restaurant = Restaurant.parse_restaurant_from_sqs(item_body)

        list_img = []
        for img in item_body['img_url']:
            img = str(img)
            if not img.__contains__('.jpg'):
                img = str(img) + ".jpg"
            list_img.append(Image(img))

        return CrawledData(
            id_post=item_body['post_id'],
            utente=item_body['username'],
            data_post=item_body['date'],
            caption=item_body['caption_text'],
            restaurant=restaurant,
            list_images=list_img)
