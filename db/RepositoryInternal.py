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
    def __set_param_emotions_confidence(emotion_confid: dict, id_img: int, num_pers: int) -> list:
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

    @staticmethod
    def __set_param_label(label: str) -> list:
        """
        Return a list of parameters for rds query

        :param label: Rekognition Label to refactor
        :return: list of parameters
        """
        return [{"name": "nome_label", "value": {"stringValue": label}}]

    @staticmethod
    def __set_param_label_img(label: str, id_img: int) -> list:
        param_list = RepositoryInternal.__set_param_label(label)
        param_list.append({"name": "id_immagine", "value": {"longValue": id_img}})
        return param_list

    @staticmethod
    def __set_param_img(id_img: int, id_post: str) -> list:
        """
        Return a list of parameters for rds query

        :param id_img: id of the image
        :return: list of parameters
        """
        param_id_img = {"name": "id_immagine", "value": {"longValue": id_img}}
        param_id_post = {"name": "id_post", "value": {"stringValue": id_post}}
        return [param_id_img, param_id_post]

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
            response = self.database.do_write_query(query_insert_label, param)[
                           'numberOfRecordsUpdated'] > 0 and response

            param = self.__set_param_label_img(label, id_img)
            response = self.database.do_write_query(query_insert_label_img, param)[
                           'numberOfRecordsUpdated'] > 0 and response

        return response

    def __save_emotions_confidence(self, emotions_confid: List[dict], id_img: int) -> bool:
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
            response = self.database.do_write_query(query_insert_emotion_img, param)[
                           'numberOfRecordsUpdated'] > 0 and response
        return response

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
            id_img = int(img.get_image_name().split('.')[0])

            param = self.__set_param_img(id_img, id_post)
            response1 = self.database.do_write_query(query, param)
            response = (response1['numberOfRecordsUpdated'] > 0) and response
            print("saved image " + img.get_image_name() + " in table immagine, response:", response)
            if img.get_labels() is not None and len(img.get_labels()) > 0:
                response = self.__save_labels(img.get_labels(), id_img) and response
            if img.get_emotions() is not None and len(img.get_emotions()) > 0:
                response = self.__save_emotions(img.get_emotions(), id_img) and response
            response = self.__save_emotions_confidence(img.get_emotions_confidence(), id_img) and response

        return response

    def __save_comprehend_score(self, score: ScoreComprehend, id_post: str) -> bool:
        query = "INSERT INTO analisi_testo (id_post, negative_comprehend, positive_comprehend, neutral_comprehend," \
                "mixed_comprehend) VALUES (:id_post, :negative, :positive,:neutral,:mixed)"

        response = self.database.do_write_query(query, score.set_param_for_query(id_post))

        return response['numberOfRecordsUpdated'] > 0

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

        response = self.database.do_write_query(query, restaurant.set_param_for_query())

        return response['numberOfRecordsUpdated'] > 0

    def save_post(self, post: CrawledData) -> bool:
        """
        Save a new post in rds and save all the relations between images, emotions, labels and itself

        :param post: post to save
        :return: boolean if queries are executed correctly
        """
        # salvo post nella tabella corrispondete
        print("saving post in table post ")

        response = True

        self.insert_new_restaurant(post.get_restaurant())

        query = "INSERT INTO post (id_post,nome_utente, data_post, id_ristorante, testo, " \
                "punteggio_emoji, punteggio_testo, punteggio_foto) VALUES " \
                "(:id_post, :post_utente, :data_post, :id_ristorante, :testo, " \
                ":punteggio_emoji, :punteggio_testo, :punteggio_foto)"

        response = self.database.do_write_query(query, post.set_param_for_query())[
                       'numberOfRecordsUpdated'] > 0 and response
        if post.get_comprehend_score() is not None:
            response = self.__save_comprehend_score(post.get_comprehend_score(), post.get_id_post()) and response

        # salvo immagini solo se presenti
        if post.get_list_images() is not None and len(post.get_list_images()) > 0:
            response = self.__save_new_images(post.get_list_images(), post.get_id_post()) and response

        return response

    def insert_new_restaurant(self, restaurant: Restaurant) -> bool:
        """
        Update restaurant info in rds, if restaurant is not present in rds it will be inserted

        :param restaurant: Restaurant to update in rds
        :return: id of restaurant inserted or updated
        """

        print("checking if restaurant already exixts in table ristorante...")

        if not self.__check_if_restaurant_already_exists(restaurant):
            response = self.__save_new_restaurant(restaurant)
            print('new restaurant inserted, response: ', response)
            return True
        else:
            print('restaurant already exists')
            return False

    def update_restaurant_scores(self, restaurant: Restaurant) -> bool:
        # if self.__check_if_restaurant_already_exists(restaurant):
        param_id = [{"name": "id", "value": {"longValue": restaurant.get_id()}}]
        new_scores = self.__recalculate_scores(param_id)

        query = "UPDATE ristorante SET " \
                "punteggio_emoji=:punteggio_emoji, " \
                "punteggio_foto=:punteggio_foto, " \
                "punteggio_testo=:punteggio_testo " \
                "WHERE id_ristorante =:id_ristorante"

        restaurant.set_image_score(new_scores['punt_foto'])
        restaurant.set_emoji_score(new_scores['punt_emoji'])
        restaurant.set_text_score(new_scores['punt_testo'])

        response = self.database.do_write_query(query, restaurant.set_param_for_query())
        print(f"restaurant scores updated: emoji: {new_scores['punt_emoji']}, "
              f"foto: {new_scores['punt_foto']}, testo:{new_scores['punt_testo']}")

        return response['numberOfRecordsUpdated'] > 0

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
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7])
            restaurant.set_emoji_score(response[8])
            restaurant.set_image_score(response[9])
            restaurant.set_text_score(response[10])
            return restaurant

        return None

    def __recalculate_scores(self, param_id: List) -> dict:
        query = 'select avg(post.punteggio_emoji) as "punt_emoji", ' \
                'avg(post.punteggio_testo) as "punt_testo", ' \
                'avg(post.punteggio_foto) as "punt_foto" ' \
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

    def __check_if_restaurant_already_exists(self, restaurant: Restaurant) -> bool:
        param = [{"name": "id_rest", "value": {"longValue": restaurant.get_id()}}]
        query = 'SELECT * FROM ristorante WHERE id_ristorante = :id_rest'
        response = self.database.do_read_query(query, param)
        return len(response) > 0
