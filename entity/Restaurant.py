class Restaurant:
    def __init__(self, id_rist: int = None, nome: str = None, indirizzo: str = None, telefono: str = None,
                 sito: str = None, lat: float = None, lng: float = None, categoria: str = None,
                 punt_emoji: float = None, punt_foto: float = None,
                 punt_testo: float = None) -> None:
        self.__id_rist = id_rist
        self.__nome = nome
        self.__indirizzo = indirizzo
        self.__telefono = telefono
        self.__sito = sito
        self.__lat = round(lat, 4)
        self.__lng = round(lng, 4)
        self.__categoria = categoria
        self.__punt_emoji = punt_emoji
        self.__punt_foto = punt_foto
        self.__punt_testo = punt_testo

    def set_punt_emoji(self, punt_emoji: int) -> None:
        self.__punt_emoji = punt_emoji

    def set_punt_foto(self, punt_foto: int) -> None:
        self.__punt_foto = punt_foto

    def set_punt_testo(self, punt_testo: int) -> None:
        self.__punt_testo = punt_testo

    def get_id_rist(self) -> int:
        return self.__id_rist

    def get_nome(self) -> str:
        return self.__nome

    def get_indirizzo(self) -> str:
        return self.__indirizzo

    def get_telefono(self) -> str:
        return self.__telefono

    def get_sito(self) -> str:
        return self.__sito

    def get_lat(self) -> float:
        return self.__lat

    def get_lng(self) -> float:
        return self.__lng

    def get_categoria(self) -> str:
        return self.__categoria

    def get_punt_emoji(self) -> float:
        return self.__punt_emoji

    def get_punt_foto(self) -> float:
        return self.__punt_foto

    def get_punt_testo(self) -> float:
        return self.__punt_testo

    def set_param_for_query(self) -> list:
        """
        Return a list of parameters for rds query

        :return: list of parameters
        """

        id_ristorante_param = {"name": "id_ristorante", "value": {"longValue": self.get_id_rist()}}
        nome_param = {"name": "nome_ristorante", "value": {"stringValue": self.get_nome()}}
        indirizzo_param = {"name": "indirizzo", "value": {"stringValue": self.get_indirizzo()}}
        telefono_param = {"name": "telefono", "value": {"stringValue": self.get_telefono()}}
        sito_param = {"name": "sito_web", "value": {"stringValue": self.get_sito()}}
        latitudine_param = {"name": "latitudine", "value": {"doubleValue": self.get_lat()}}
        longitudine_param = {"name": "longitudine", "value": {"doubleValue": self.get_lng()}}
        categoria_param = {"name": "categoria", "value": {"stringValue": self.get_categoria()}}
        punteggio_emoji_param = {"name": "punteggio_emoji", "value": {"doubleValue": self.get_punt_emoji()}}
        punteggio_foto_param = {"name": "punteggio_foto", "value": {"doubleValue": self.get_punt_foto()}}
        punteggio_testo_param = {"name": "punteggio_testo", "value": {"doubleValue": self.get_punt_testo()}}

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
            self.__id_rist) + " \n" + \
               self.__nome + " \n" + \
               self.__indirizzo + " \n" + \
               self.__telefono + " \n" + \
               self.__sito + "\n" + \
               str(self.__lat) + " \n" + \
               str(self.__lng) + " \n" + \
               self.__categoria + " \n" + \
               str(self.__punt_emoji) + " \n" + \
               str(self.__punt_foto) + " \n" + \
               str(self.__punt_testo)
