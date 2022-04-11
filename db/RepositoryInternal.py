from db.Database import Database
from entity.Restaurant import Restaurant
from entity.CrawledData import CrawledData
import logging


class RepositoryInternal:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = Database(db_name)

    @staticmethod
    def __set_param_restaurant(restaurant: Restaurant) -> list:
        nome_param = {"name": "nome_ristorante", "value": {"stringValue": restaurant.nome}}
        indirizzo_param = {"name": "indirizzo", "value": {"stringValue": restaurant.indirizzo}}
        telefono_param = {"name": "telefono", "value": {"stringValue": restaurant.telefono}}
        sito_param = {"name": "sito_web", "value": {"stringValue": restaurant.sito}}
        latitudine_param = {"name": "latitudine", "value": {"doubleValue": restaurant.lat}}
        longitudine_param = {"name": "longitudine", "value": {"doubleValue": restaurant.lng}}
        categoria_param = {"name": "categoria", "value": {"stringValue": restaurant.categoria}}

        if restaurant.punt_emoji is None:
            punteggio_emoji_param = {"name": "punteggio_emoji", "value": {"longValue": 0}}
        else:
            punteggio_emoji_param = {"name": "punteggio_emoji", "value": {"longValue": restaurant.punt_emoji}}

        if restaurant.punt_foto is None:
            punteggio_foto_param = {"name": "punteggio_foto", "value": {"longValue": 0}}
        else:
            punteggio_foto_param = {"name": "punteggio_foto", "value": {"longValue": restaurant.punt_foto}}

        if restaurant.punt_testo is None:
            punteggio_testo_param = {"name": "punteggio_testo", "value": {"longValue": 0}}
        else:
            punteggio_testo_param = {"name": "punteggio_testo", "value": {"longValue": restaurant.punt_testo}}

        id_rest_param = {"name": "id", "value": {"longValue": restaurant.id_rist}}

        return [nome_param, indirizzo_param, telefono_param, sito_param, latitudine_param, longitudine_param,
                categoria_param, punteggio_emoji_param, punteggio_foto_param, punteggio_testo_param, id_rest_param]

    @staticmethod
    def __set_param_crawled_data(post: CrawledData) -> list:
        post_utente_param = {"name": "post_utente", "value": {"stringValue": post.utente}}
        data_post_param = {"name": "data_post", "value": {"stringValue": str(post.data_post)}, "typeHint": "TIMESTAMP"}
        restaurant_param = {"name": "id_ristorante", "value": {"longValue": post.restaurant.id_rist}}
        caption_param = {"name": "testo", "value": {"stringValue": post.caption}}

        if post.punt_emoji is None:
            emoji_param = {"name": "punteggio_emoji", "value": {"isNull": True}}
        else:
            emoji_param = {"name": "punt_emoji", "value": {"longValue": post.punt_emoji}}

        score_param = {"name": "score", "value": {"longValue": post.score.calculate_score}}
        negative_param = {"name": "negative", "value": {"longValue": post.score.negative}}
        positive_param = {"name": "positive", "value": {"longValue": post.score.positive}}
        neutral_param = {"name": "neutral", "value": {"longValue": post.score.neutral}}

        return [post_utente_param, data_post_param, restaurant_param, caption_param, emoji_param, score_param,
                negative_param, positive_param, neutral_param]

    @staticmethod
    def __set_param_emotion(emotions: str) -> list:
        param_list = []
        param = {"name": "nome_emozione", "value": {"stringValue": emotions}}
        param_list.append(param)
        return param_list

    @staticmethod
    def __set_param_emotion_img(emotions: str, id_img: int, qta: int) -> list:
        param_list = RepositoryInternal.__set_param_emotion(emotions)
        param = {"name": "id_immagine", "value": {"longValue": id_img}}
        param_list.append(param)
        param = {"name": "qta", "value": {"longValue": qta}}
        param_list.append(param)
        return param_list

    @staticmethod
    def __set_param_label(label: str) -> list:
        param_list = []
        param = {"name": "nome_label", "value": {"stringValue": label}}
        param_list.append(param)
        return param_list

    @staticmethod
    def __set_param_label_img(label: str, id_img: int, qta: int) -> list:
        param_list = RepositoryInternal.__set_param_label(label)
        param = {"name": "id_immagine", "value": {"longValue": id_img}}
        param_list.append(param)
        param = {"name": "qta", "value": {"longValue": qta}}
        param_list.append(param)
        return param_list

    def __save_new_restaurant(self, restaurant: Restaurant) -> int:

        query = "INSERT INTO ristorante (nome_ristorante, indirizzo, telefono, sito_web, " \
                "latitudine, longitudine, categoria,punteggio_emoji, punteggio_foto, " \
                "punteggio_testo) VALUES ( :name, :indirizzo, :telefono, :sito_web, :latitudine, :longitudine, " \
                ":categoria, :punteggio_emoji, :punteggio_foto, :punteggio_testo)"

        response = self.database.do_write_query(query, self.__set_param_restaurant(restaurant))
        return response

    def __save_new_images(self, list_images: list, id_post: int) -> bool:
        query = "INSERT INTO immaigini (id_immagine, id_post) VALUES (%s, %s)"
        response = True

        for img in list_images:
            values = (img, id_post)
            response = response and (self.database.do_write_query(query, values) > 0)

        return response

    def __save_emotions(self, emotions: dict, list_images: list) -> bool:
        query_insert_emotions = "INSERT INTO emozioni VALUES :nome_emozione"
        query_insert_emotions_img = "INSERT INTO emozioni_img VALUES :id_immagine, :nome_emozione, :qta"

        response = True

        for img in list_images:
            for key, value in emotions.items():
                param = self.__set_param_emotion(key)
                response = response and (self.database.do_write_query(query_insert_emotions, param) > 0)

                param = self.__set_param_emotion_img(key, list_images[0], value)
                response = response and (self.database.do_write_query(query_insert_emotions_img, param) > 0)

        return response

    def __save_labels(self, labels: dict, list_images: list) -> bool:
        query = "INSERT INTO labels VALUES :labels"
        response = self.database.do_write_query(query, self.__set_param_label(labels)) > 0

        return response

    def save_post(self, post: CrawledData) -> bool:

        # salvo post nella tabella corrispondete
        print("save post in table post")
        query = "INSERT INTO post (nome_utente, data_post, id_ristorante, testo, punteggio_emoji, " \
                "score, negative_comprehend, positive_comprehend, neutral_comprehend)" \
                "VALUES (:post_utente, :data_post, :id_ristorante, :testo, :punt_emoji, :score, :negative, " \
                ":positive, :neutral)"

        response = self.database.do_write_query(query, self.__set_param_crawled_data(post)) > 0

        # salvo immagini solo se presenti
        if post.list_image is not None:
            print("save images in table immagini")
            response = response and self.__save_new_images(post.list_image, post.id_post)

            # salvare emozioni trovate con comprehend
            response = response and self.__save_emotions(post.emotions, post.list_image)

            # salvare labels trovati con rekognition
            response = response and self.__save_labels(post.labels, post.list_image)

        return response

    def update_restaurant_info(self, restaurant: Restaurant) -> int:

        query = "UPDATE ristorante SET " \
                "nome_ristorante=:nome_param, " \
                "indirizzo=:indirizzo_param, " \
                "telefono=:telefono_param, " \
                "sito_web=:sito_param, " \
                "latitudine=:latitudine_param, " \
                "longitudine=:longitudine_param, " \
                "categoria=:categoria_param, " \
                "punteggio_emoji=:punteggio_emoji_param, " \
                "punteggio_foto=:punteggio_foto_param, " \
                "punteggio_testo=:punteggio_testo_param " \
                "WHERE id=:id_rest_param"

        response = self.database.do_write_query(query, self.__set_param_restaurant(restaurant))
        return response

    def get_restaurant_info_by_name(self, name: str) -> Restaurant:
        param = {"name": "nome_ristorante", "value": {"stringValue": '%' + name + '%'}}

        query = "SELECT * FROM ristorante WHERE nome_ristorante LIKE :name"
        response = self.database.do_read_query(query, param)
        if response is not None:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return Restaurant()

    # !!! stesso codice di RepositoryExternal.py !!! #
    def get_restaurant_info_by_id(self, id_restaurant: int) -> Restaurant:

        param = {"name": "id_restaurant", "value": {"longValue": id_restaurant}}

        query = "SELECT * FROM ristorante WHERE id_ristorante = :id_restaurant"

        response = self.database.do_read_query(query, param)
        if response is not None:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return Restaurant()
