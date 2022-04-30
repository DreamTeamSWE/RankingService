class Restaurant:
    def __init__(self, id_rist: int, nome: str, lat: float, lng: float, indirizzo: str = None, telefono: str = None,
                 sito: str = None, categoria: str = None) -> None:
        self.__id = id_rist
        self.__name = nome
        self.__address = indirizzo
        self.__phone = telefono
        self.__website = sito
        self.__lat = round(lat, 4)
        self.__lng = round(lng, 4)
        self.__category = categoria
        self.__emoji_score = None
        self.__image_score = None
        self.__text_score = None

    def set_emoji_score(self, punt_emoji: float) -> None:
        self.__emoji_score = punt_emoji

    def set_image_score(self, punt_foto: float) -> None:
        self.__image_score = punt_foto

    def set_text_score(self, punt_testo: float) -> None:
        self.__text_score = punt_testo

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_address(self) -> str:
        return self.__address

    def get_phone(self) -> str:
        return self.__phone

    def get_website(self) -> str:
        return self.__website

    def get_lat(self) -> float:
        return self.__lat

    def get_lng(self) -> float:
        return self.__lng

    def get_category(self) -> str:
        return self.__category

    def get_emoji_score(self) -> float:
        return self.__emoji_score

    def get_image_score(self) -> float:
        return self.__image_score

    def get_text_score(self) -> float:
        return self.__text_score

    def set_param_for_query(self) -> list:
        """
        Return a list of parameters for rds query

        :return: list of parameters
        """

        id_ristorante_param = {"name": "id_ristorante", "value": {"longValue": self.get_id()}}
        nome_param = {"name": "nome_ristorante", "value": {"stringValue": self.get_name()}}
        indirizzo_param = {"name": "indirizzo", "value": {"stringValue": self.get_address()}}
        telefono_param = {"name": "telefono", "value": {"stringValue": self.get_phone()}}
        sito_param = {"name": "sito_web", "value": {"stringValue": self.get_website()}}
        latitudine_param = {"name": "latitudine", "value": {"doubleValue": self.get_lat()}}
        longitudine_param = {"name": "longitudine", "value": {"doubleValue": self.get_lng()}}
        categoria_param = {"name": "categoria", "value": {"stringValue": self.get_category()}}
        punteggio_emoji_param = {"name": "punteggio_emoji", "value": {"doubleValue": self.get_emoji_score()}}
        punteggio_foto_param = {"name": "punteggio_foto", "value": {"doubleValue": self.get_image_score()}}
        punteggio_testo_param = {"name": "punteggio_testo", "value": {"doubleValue": self.get_text_score()}}

        return [id_ristorante_param, nome_param, indirizzo_param, telefono_param, sito_param, latitudine_param,
                longitudine_param, categoria_param, punteggio_emoji_param, punteggio_foto_param, punteggio_testo_param]

    @staticmethod
    def parse_restaurant_from_sqs(item: dict):
        """
        parse json from sqs to get restaurant object

        :param item: object from sqs
        :return: restaurant object
        :rtype: Restaurant
        """
        json_restaurant = item['location']

        return Restaurant(
            id_rist=json_restaurant['db_id'],
            nome=json_restaurant['location_name'],
            indirizzo="",  # json_restaurant['address'],
            telefono=json_restaurant['phone'],
            sito=json_restaurant['website'],
            lat=json_restaurant['lat'],
            lng=json_restaurant['lng'],
            categoria=json_restaurant['category']
        )

    def __str__(self) -> str:
        return "Restaurant: " + str(
            self.__id) + " \n" + \
               self.__name + " \n" + \
               self.__address + " \n" + \
               self.__phone + " \n" + \
               self.__website + "\n" + \
               str(self.__lat) + " \n" + \
               str(self.__lng) + " \n" + \
               self.__category + " \n" + \
               str(self.__emoji_score) + " \n" + \
               str(self.__image_score) + " \n" + \
               str(self.__text_score)
