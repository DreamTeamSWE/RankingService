from typing import List
from datetime import datetime

from entity.Restaurant import Restaurant
from entity.ScoreComprehend import ScoreComprehend
from entity.Image import Image


class CrawledData:
    def __init__(self, id_post: str = None, utente: str = None,
                 data_post: str = datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), caption: str = None,
                 restaurant: Restaurant = None, list_images: List[Image] = None) -> None:
        self.__id_post = id_post
        self.__utente = utente
        self.__data_post = data_post
        self.__caption = caption
        self.__restaurant = restaurant
        self.__list_images = list_images
        self.__punt_emoji = None
        self.__punt_foto = None
        self.__punt_testo = None
        self.__comprehend_score = None

    def set_punt_testo(self):
        if self.__comprehend_score:
            self.__punt_testo = self.__comprehend_score.calculate_score()

    def calculate_and_set_punt_foto(self):
        if self.__list_images:
            for image in self.__list_images:
                score = image.calculate_score()
                if score is not None:
                    self.__punt_foto = (self.__punt_foto + score) if self.__punt_foto is not None else score

    def set_punt_emoji(self, punt_emoji: float):
        self.__punt_emoji = punt_emoji

    def set_comprehend_score(self, score: ScoreComprehend):
        self.__comprehend_score = score

    def get_id_post(self) -> str:
        return self.__id_post

    def get_utente(self) -> str:
        return self.__utente

    def get_data_post(self) -> str:
        return self.__data_post

    def get_caption(self) -> str:
        return self.__caption

    def get_list_images(self) -> List[Image]:
        return self.__list_images

    def get_restaurant(self) -> Restaurant:
        return self.__restaurant

    def get_comprehend_score(self) -> ScoreComprehend:
        return self.__comprehend_score

    @staticmethod
    def parse_post_from_sqs(item_body: dict) -> 'CrawledData':
        restaurant = Restaurant.parse_restaurant_from_sqs(item_body)

        # modifiche temporanee
        list_img = []
        if 's3_id' in item_body:
            for img in item_body['s3_id']:
                img = str(img)
                if not img.__contains__('.jpg'):
                    img = str(img) + ".jpg"
                list_img.append(Image(img))

            return CrawledData(
                id_post=item_body['post_id'],
                utente=item_body['username'],
                data_post=item_body['date'][0:10],
                caption=item_body['caption_text'],
                restaurant=restaurant,
                list_images=list_img)

        elif 'img_url' in item_body:
            for img in item_body['img_url']:
                img = str(img)
                if not img.__contains__('.jpg'):
                    img = str(img) + ".jpg"
                list_img.append(Image(img))

            return CrawledData(
                id_post=item_body['post_id'],
                utente=item_body['username'],
                data_post=item_body['date'][0:10],
                caption=item_body['caption_text'],
                restaurant=restaurant,
                list_images=list_img)

    def set_param_for_query(self) -> list:
        """
        Return a list of parameters for rds query

        :return: list of parameters
        """

        id_post_param = {"name": "id_post", "value": {"stringValue": self.__id_post}}
        post_utente_param = {"name": "post_utente", "value": {"stringValue": self.__utente}}
        data_post_param = {"name": "data_post", "value": {"stringValue": str(self.__data_post)}, "typeHint": "DATE"}
        restaurant_param = {"name": "id_ristorante", "value": {"longValue": self.__restaurant.get_id_rist()}}
        caption_param = {"name": "testo", "value": {"stringValue": self.__caption}}
        emoji_param = {"name": "punteggio_emoji", "value": {"doubleValue": self.__punt_emoji}}
        punt_testo_param = {"name": "punteggio_testo", "value": {"doubleValue": self.__punt_testo}}
        punt_foto_param = {"name": "punteggio_foto", "value": {"doubleValue": self.__punt_foto}}
        param_list = [id_post_param, post_utente_param, data_post_param, restaurant_param, caption_param, emoji_param,
                      punt_testo_param, punt_foto_param]

        return param_list

    def __str__(self):
        return "id_post: " + str(self.__id_post) + "\n" + \
               "utente: " + str(self.__utente) + "\n" + \
               "data_post: " + str(self.__data_post) + "\n" + \
               "caption: " + str(self.__caption) + "\n" + \
               "list_image: " + str(self.__list_images) + "\n" + \
               "restaurant: " + str(self.__restaurant) + "\n" + \
               "punt_emoji: " + str(self.__punt_emoji) + "\n" + \
               "punt_foto: " + str(self.__punt_foto) + "\n" + \
               "punt_testo: " + str(self.__punt_testo)
