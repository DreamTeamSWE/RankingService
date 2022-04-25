from typing import Optional, List
from db.DatabaseHandler import DatabaseHandler
from entity.ScoreComprehend import ScoreComprehend
from entity.CrawledData import CrawledData
from entity.Restaurant import Restaurant
from entity.Image import Image


class RepositoryInternal:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    @staticmethod
    def __set_param_restaurant(restaurant: Restaurant) -> list:
        """
        Return a list of parameters for rds query

        :param restaurant: Restaurant to refactor
        :return: list of parameters
        """
        id_ristorante_param = {"name": "id_ristorante", "value": {"longValue": restaurant.id_rist}}
        nome_param = {"name": "nome_ristorante", "value": {"stringValue": restaurant.nome}}
        indirizzo_param = {"name": "indirizzo", "value": {"stringValue": restaurant.indirizzo}}
        telefono_param = {"name": "telefono", "value": {"stringValue": restaurant.telefono}}
        sito_param = {"name": "sito_web", "value": {"stringValue": restaurant.sito}}
        latitudine_param = {"name": "latitudine", "value": {"doubleValue": restaurant.lat}}
        longitudine_param = {"name": "longitudine", "value": {"doubleValue": restaurant.lng}}
        categoria_param = {"name": "categoria", "value": {"stringValue": restaurant.categoria}}
        punteggio_emoji_param = {"name": "punteggio_emoji", "value": {"doubleValue": restaurant.punt_emoji}}
        punteggio_foto_param = {"name": "punteggio_foto", "value": {"doubleValue": restaurant.punt_foto}}
        punteggio_testo_param = {"name": "punteggio_testo", "value": {"doubleValue": restaurant.punt_testo}}

        return [id_ristorante_param, nome_param, indirizzo_param, telefono_param, sito_param, latitudine_param,
                longitudine_param, categoria_param, punteggio_emoji_param, punteggio_foto_param, punteggio_testo_param]

    @staticmethod
    def __set_param_crawled_data(post: CrawledData) -> list:
        """
        Return a list of parameters for rds query

        :param post: Post if IG to refactor
        :return: list of parameters
        """

        id_post_param = {"name": "id_post", "value": {"stringValue": post.id_post}}
        post_utente_param = {"name": "post_utente", "value": {"stringValue": post.utente}}
        data_post_param = {"name": "data_post", "value": {"stringValue": str(post.data_post)}, "typeHint": "DATE"}
        restaurant_param = {"name": "id_ristorante", "value": {"longValue": post.restaurant.id_rist}}
        caption_param = {"name": "testo", "value": {"stringValue": post.caption}}
        emoji_param = {"name": "punteggio_emoji", "value": {"doubleValue": post.punt_emoji}}
        punt_testo_param = {"name": "punteggio_testo", "value": {"doubleValue": post.punt_testo.calculate_score()}}
        punt_foto_param = {"name": "punteggio_foto", "value": {"doubleValue": post.punt_foto}}
        param_list = [id_post_param, post_utente_param, data_post_param, restaurant_param, caption_param, emoji_param,
                      punt_testo_param, punt_foto_param]

        return param_list

    @staticmethod
    def __set_param_comprehend_score(score: ScoreComprehend, id_post: str):
        post_id = {"name": "id_post", "value": {"stringValue": id_post}}
        negative_param = {"name": "negative", "value": {"longValue": score.negative}}
        positive_param = {"name": "positive", "value": {"longValue": score.positive}}
        neutral_param = {"name": "neutral", "value": {"longValue": score.neutral}}
        mixed_param = {"name": "mixed", "value": {"longValue": score.mixed}}
        return [post_id, negative_param, positive_param, neutral_param, mixed_param]

    @staticmethod
    def __set_param_emotions_confidence(emotion_confid: dict, id_img: int, num_pers: int):
        param_list = []
        names = ['happy', 'calm', 'sad', 'angry', 'surprised', 'confused', 'disgusted', 'fear']

        for name in names:
            param_list.append({"name": name, "value": {"doubleValue": emotion_confid[name.upper()]}})

        num_persona_param = {"name": "num_persona", "value": {"longValue": num_pers}}
        param_list.append(num_persona_param)
        id_img_param = {"name": "id_immagine", "value": {"longValue": id_img}}
        param_list.append(id_img_param)
        return param_list

    @staticmethod
    def __set_param_emotion(emotion: str) -> list:
        """
        Return a list of parameters for rds query

        :param emotion: Rekognition Emotions to refactor
        :return: list of parameters
        """
        return [{"name": "nome_emozione", "value": {"stringValue": emotion}}]

    @staticmethod
    def __set_param_emotion_img(emotion: str, id_img: int, qta: int) -> list:
        """
        Return a list of parameters for rds query

        :param emotion: Rekognition Emotions to refactor
        :param id_img: id of image to refactor
        :param qta: quantity of emotions to refactor
        :return: list of parameters
        """
        param_list = RepositoryInternal.__set_param_emotion(emotion)
        param_list.append({"name": "id_immagine", "value": {"longValue": id_img}})
        param_list.append({"name": "qta", "value": {"longValue": qta}})
        return param_list

    # check
    # da testare
    @staticmethod
    def __set_param_label(label: str) -> list:
        """
        Return a list of parameters for rds query

        :param label: Rekognition Label to refactor
        :return: list of parameters
        """
        return [{"name": "nome_label", "value": {"stringValue": label}}]

    # check
    # da testare
    @staticmethod
    def __set_param_label_img(label: str, id_img: int, confidenza: float = None) -> list:
        param_list = RepositoryInternal.__set_param_label(label)
        param_list.append({"name": "id_immagine", "value": {"longValue": id_img}})
        return param_list

    @staticmethod  # check
    # da testare
    def __set_param_img(id_img: int, id_post: str) -> list:
        """
        Return a list of parameters for rds query

        :param id_img: id of the image
        :return: list of parameters
        """
        param_id_img = {"name": "id_immagine", "value": {"longValue": id_img}}
        param_id_post = {"name": "id_post", "value": {"stringValue": id_post}}
        return [param_id_img, param_id_post]

    # check
    # da testare
    def __save_labels(self, labels: dict, id_img: int) -> bool:
        """
        Save new labels in rds and save the relation between the image and labels

        :param labels: labels to save
        :param id_img: id of the image
        :return: boolean if queries are executed correctly
        """
        query_insert_label = "INSERT IGNORE INTO label VALUES (:nome_label)"
        query_insert_label_img = "INSERT INTO label_img(id_immagine, nome_label) VALUES " \
                                 "(:id_immagine, :nome_label)"

        response = True

        # iterate over all labels names (keys)
        print('labels - ' + str(id_img))
        print(labels)

        for label in labels:
            param = self.__set_param_label(label)
            response = self.database.do_write_query(query_insert_label, param)['numberOfRecordsUpdated'] > 0 and response

            param = self.__set_param_label_img(label, id_img)
            response = self.database.do_write_query(query_insert_label_img, param)['numberOfRecordsUpdated'] > 0 and response

        return response

    def __save_emotions_confidence(self, emotions_confid: List[dict], id_img: int):
        if emotions_confid:
            query = 'INSERT INTO confidenza_emozioni(happy, calm, sad, angry, surprised, confused, disgusted, fear,' \
                    'num_persona, id_immagine) VALUES (:happy, :calm, :sad, :angry, :surprised, ' \
                    ':confused, :disgusted,:fear, :num_persona, :id_immagine) '
            response = True
            count = 0  # per generare l'indice della faccia
            for face in emotions_confid:
                response = self.database.do_write_query(query,
                                                        self.__set_param_emotions_confidence(face, id_img, count)
                                                        )['numberOfRecordsUpdated'] > 0 and response
                count += 1
            return response

    # check
    # da testare
    def __save_emotions(self, emotions: dict, id_img: int) -> bool:
        """
        Save new emotions in rds and save the relation between images and emotions

        :param emotions: emotions to save
        :param id_img: id of images to save
        :return: boolean if queries are executed correctly
        """

        query_insert_emotion_img = "INSERT INTO emozione_img VALUES (:id_immagine, :nome_emozione, :qta)"

        response = True

        print(emotions)

        for emotion in emotions:
            print(emotion)
            param = self.__set_param_emotion_img(emotion=emotion, id_img=id_img, qta=emotions[emotion])
            response = self.database.do_write_query(query_insert_emotion_img, param)['numberOfRecordsUpdated'] > 0 and response
        return response

    # check
    # da testare
    def __save_new_images(self, list_images: List[Image], id_post: str) -> bool:
        """
        Save a new images and its labels and emotions if presents in rds

        :param list_images: list of images to save
        :param id_post: id of post to save
        :return: boolean if queries are executed correctly
        """
        query = "INSERT INTO immagine (id_immagine, id_post) VALUES (:id_immagine, :id_post)"
        response = True

        for img in list_images:
            # remove extension from image name and convert to int
            id_img = int(img.image_name.split('.')[0])

            param = self.__set_param_img(id_img, id_post)
            response = (self.database.do_write_query(query, param))['numberOfRecordsUpdated'] > 0 and response
            print("saved image " + img.image_name + " in table immagine, response:", response)
            if img.labels is not None and len(img.labels) > 0:
                response = self.__save_labels(img.labels, id_img) and response
            if img.emotions is not None and len(img.emotions) > 0:
                response = self.__save_emotions(img.emotions, id_img) and response
            response = self.__save_emotions_confidence(img.emotions_confidence, id_img) and response

        return response

    def __save_comprehend_score(self, score: ScoreComprehend, id_post: str) -> bool:
        query = "INSERT INTO analisi_testo (id_post, negative_comprehend, positive_comprehend, neutral_comprehend," \
                "mixed_comprehend) VALUES (:id_post, :negative, :positive,:neutral,:mixed)"

        response = self.database.do_write_query(query, self.__set_param_comprehend_score(score, id_post))

        return response['numberOfRecordsUpdated'] > 0

    # check
    # da testare
    def save_post(self, post: CrawledData) -> bool:
        """
        Save a new post in rds and save all the relations between images, emotions, labels and itself

        :param post: post to save
        :return: boolean if queries are executed correctly
        """
        # salvo post nella tabella corrispondete
        print("saving post in table post ")

        response = True

        response = self.update_restaurant_info(post.restaurant) and response

        query = "INSERT INTO post (id_post,nome_utente, data_post, id_ristorante, testo, " \
                "punteggio_emoji, punteggio_testo, punteggio_foto) VALUES " \
                "(:id_post, :post_utente, :data_post, :id_ristorante, :testo, " \
                ":punteggio_emoji, :punteggio_testo, :punteggio_foto)"

        response = self.database.do_write_query(query,
                                                self.__set_param_crawled_data(post))['numberOfRecordsUpdated'] > 0 and response

        response =  self.__save_comprehend_score(post.punt_testo, post.id_post) and response

        # salvo immagini solo se presenti
        if post.list_images:
            response = self.__save_new_images(post.list_images, post.id_post) and response

        return response

    def __save_new_restaurant(self, restaurant: Restaurant) -> bool:
        """
        Save a new restaurant in rds
        :param restaurant: Restaurant to save
        :return: boolean if the restaurant is saved
        """

        print("saving restaurant in table ristorante")

        query = "INSERT INTO ristorante (id_ristorante, nome_ristorante, indirizzo, telefono, sito_web, " \
                "latitudine, longitudine, categoria, punteggio_emoji, punteggio_foto, " \
                "punteggio_testo) VALUES (:id_ristorante, :nome_ristorante, :indirizzo, :telefono, :sito_web, " \
                ":latitudine, :longitudine, :categoria, :punteggio_emoji, :punteggio_foto, :punteggio_testo)"

        response = \
            self.database.do_write_query(query, self.__set_param_restaurant(restaurant))['numberOfRecordsUpdated'] > 0

        return response

    def update_restaurant_info(self, restaurant: Restaurant) -> bool:
        """
        Update restaurant info in rds, if restaurant is not present in rds it will be inserted

        :param restaurant: Restaurant to update in rds
        :return: id of restaurant inserted or updated
        """
        print("updating restaurant in table ristorante")

        if self._check_if_restaurant_already_exists(restaurant):
            # aggiorno il ristorante
            param_id = [{"name": "id", "value": {"longValue": restaurant.id_rist}}]
            new_scores = self._recalculate_scores(param_id)

            query = "UPDATE ristorante SET " \
                    "nome_ristorante=:nome_ristorante, " \
                    "indirizzo=:indirizzo, " \
                    "telefono=:telefono, " \
                    "sito_web=:sito_web, " \
                    "latitudine=:latitudine, " \
                    "longitudine=:longitudine, " \
                    "categoria=:categoria, " \
                    "punteggio_emoji=:punteggio_emoji, " \
                    "punteggio_foto=:punteggio_foto, " \
                    "punteggio_testo=:punteggio_testo " \
                    "WHERE id_ristorante =:id_ristorante"

            restaurant.set_punt_foto(new_scores['punt_foto'])
            restaurant.set_punt_emoji(new_scores['punt_emoji'])
            restaurant.set_punt_testo(new_scores['punt_testo'])

            response = \
                self.database.do_write_query(query, self.__set_param_restaurant(restaurant))['numberOfRecordsUpdated'] > 0

            print("restaurant already exists, response update restaurant: ", response)

        else:
            response = self.__save_new_restaurant(restaurant)
            print('new restaurant inserted, response: ', response)

        return response

    def get_restaurant_info_by_name(self, name: str) -> Optional[Restaurant]:
        """
        Get restaurant info from rds by name

        :param name: name of restaurant
        :return: Restaurant found or None
        """
        param = {"name": "nome_ristorante", "value": {"stringValue": '%' + name + '%'}}

        query = "SELECT * FROM ristorante WHERE nome_ristorante LIKE :name"
        response = self.database.do_read_query(query, param)
        if response['numberOfRecordsUpdated'] > 0:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return None

    # !!! stesso codice di RepositoryExternal.py !!! #
    def get_restaurant_info_by_id(self, id_restaurant: int) -> Optional[Restaurant]:
        """
        Get restaurant info from rds by id

        :param id_restaurant: id of restaurant to get from rds
        :return: Restaurant found or None
        """

        param = {"name": "id_restaurant", "value": {"longValue": id_restaurant}}

        query = "SELECT * FROM ristorante WHERE id_ristorante = :id_restaurant"

        response = self.database.do_read_query(query, param)
        if response['numberOfRecordsUpdated'] > 0:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return None

    def _recalculate_scores(self, param_id: List):
        query = 'select sum(post.punteggio_emoji)/count(*) as "punt_emoji", ' \
                'sum(post.punteggio_testo)/count(*) as "punt_testo", ' \
                'sum(post.punteggio_foto)/count(*) as "punt_foto" ' \
                'from ristorante join post on ' \
                'ristorante.id_ristorante = post.id_ristorante where ristorante.id_ristorante = :id '

        response = self.database.do_read_query(query, param_id)
        return response[0]

    def check_if_post_already_exist(self, id_post: str) -> bool:
        """
        check if a post is already saved in db

        :param id_post: id of post to check
        :return: True if post is already saved, False otherwise
        """
        param = [{"name": "id_post", "value": {"stringValue": id_post}}]
        query = "SELECT * FROM post WHERE id_post = :id_post"
        response = self.database.do_read_query(query, param)
        return len(response) > 0

    def _check_if_restaurant_already_exists(self, restaurant):
        param = [{"name": "id_rest", "value": {"longValue": restaurant.id_rist}}]
        query = 'SELECT * FROM ristorante WHERE id_ristorante = :id_rest'
        response = self.database.do_read_query(query, param)
        return len(response) > 0
