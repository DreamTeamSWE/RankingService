from typing import List
from datetime import datetime

from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend
from entity.Image import Image


class CrawledData:
    def __init__(self, id_post: str = None, author: str = None,
                 date_post: str = datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), caption: str = None,
                 restaurant: Restaurant = None, list_images: List[Image] = None) -> None:
        self.__id_post = id_post
        self.__author = author
        self.__date_post = date_post
        self.__caption = caption
        self.__restaurant = restaurant
        self.__list_images = list_images
        self.__emoji_score = None
        self.__image_score = None
        self.__text_score = None
        self.__comprehend_score = None

    def calculate_and_set_text_score(self):
        if self.__comprehend_score:
            self.__text_score = self.__comprehend_score.calculate_score()

    def calculate_and_set_image_score(self):
        if self.__list_images:
            count = 0
            for image in self.__list_images:
                score = image.calculate_score()
                if score is not None:
                    count += 1
                    self.__image_score = (self.__image_score + score) if self.__image_score is not None else score
            if self.__image_score:
                self.__image_score = self.__image_score / count

    def set_emoji_score(self, punt_emoji: float):
        self.__emoji_score = punt_emoji

    def set_comprehend_score(self, score: ScoreComprehend):
        self.__comprehend_score = score

    def get_id_post(self) -> str:
        return self.__id_post

    def get_author(self) -> str:
        return self.__author

    def get_date_post(self) -> str:
        return self.__date_post

    def get_caption(self) -> str:
        return self.__caption

    def get_list_images(self) -> List[Image]:
        return self.__list_images

    def get_restaurant(self) -> Restaurant:
        return self.__restaurant

    def get_comprehend_score(self) -> ScoreComprehend:
        return self.__comprehend_score

    def get_image_score(self) -> float:
        return self.__image_score

    @staticmethod
    def parse_post_from_sqs(item_body: dict) -> 'CrawledData':
        restaurant = Restaurant.parse_restaurant_from_sqs(item_body)

        list_img = []
        if 's3_id' in item_body:
            for img in item_body['s3_id']:
                img = str(img)
                if not img.__contains__('.jpg'):
                    img = str(img) + ".jpg"
                list_img.append(Image(img))

            return CrawledData(
                id_post=item_body['post_id'],
                author=item_body['username'],
                date_post=item_body['date'][0:10],
                caption=item_body['caption_text'],
                restaurant=restaurant,
                list_images=list_img)

        # elif 'img_url' in item_body:
        #     for img in item_body['img_url']:
        #         img = str(img)
        #         if not img.__contains__('.jpg'):
        #             img = str(img) + ".jpg"
        #         list_img.append(Image(img))
        #
        #     return CrawledData(
        #         id_post=item_body['post_id'],
        #         author=item_body['username'],
        #         date_post=item_body['date'][0:10],
        #         caption=item_body['caption_text'],
        #         restaurant=restaurant,
        #         list_images=list_img)

    def set_param_for_query(self) -> list:
        """
        Return a list of parameters for rds query

        :return: list of parameters
        """

        id_post_param = {"name": "id_post", "value": {"stringValue": self.__id_post}}
        post_author_param = {"name": "post_utente", "value": {"stringValue": self.__author}}
        data_post_param = {"name": "data_post", "value": {"stringValue": str(self.__date_post)}, "typeHint": "DATE"}
        restaurant_param = {"name": "id_ristorante", "value": {"longValue": self.__restaurant.get_id()}}
        caption_param = {"name": "testo", "value": {"stringValue": self.__caption}}
        emoji_param = {"name": "punteggio_emoji", "value": {"doubleValue": self.__emoji_score}}
        punt_testo_param = {"name": "punteggio_testo", "value": {"doubleValue": self.__text_score}}
        punt_foto_param = {"name": "punteggio_foto", "value": {"doubleValue": self.__image_score}}
        param_list = [id_post_param, post_author_param, data_post_param, restaurant_param, caption_param, emoji_param,
                      punt_testo_param, punt_foto_param]

        return param_list

    def __str__(self):
        return "id_post: " + str(self.__id_post) + "\n" + \
               "utente: " + str(self.__author) + "\n" + \
               "data_post: " + str(self.__date_post) + "\n" + \
               "caption: " + str(self.__caption) + "\n" + \
               "list_image: " + str(self.__list_images) + "\n" + \
               "restaurant: " + str(self.__restaurant) + "\n" + \
               "punt_emoji: " + str(self.__emoji_score) + "\n" + \
               "punt_foto: " + str(self.__image_score) + "\n" + \
               "punt_testo: " + str(self.__text_score)
