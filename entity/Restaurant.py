class Restaurant:
    def __init__(self, id_rist: int = None, nome: str = None, indirizzo: str = None, telefono: str = None,
                 sito: str = None, lat: float = None, lng: float = None, categoria: str = None,
                 punt_emoji: float = None, punt_foto: float = None,
                 punt_testo: float = None) -> None:
        self.id_rist = id_rist
        self.nome = nome
        self.indirizzo = indirizzo
        self.telefono = telefono
        self.sito = sito
        self.lat = round(lat, 4)
        self.lng = round(lng, 4)
        self.categoria = categoria
        self.punt_emoji = punt_emoji
        self.punt_foto = punt_foto
        self.punt_testo = punt_testo

    def set_punt_emoji(self, punt_emoji: int) -> None:
        self.punt_emoji = punt_emoji

    def set_punt_foto(self, punt_foto: int) -> None:
        self.punt_foto = punt_foto

    def set_punt_testo(self, punt_testo: int) -> None:
        self.punt_testo = punt_testo

    def __str__(self):
        return "Restaurant: " + str(
            self.id_rist) + " \n" + self.nome + " \n" + self.indirizzo + " \n" + self.telefono + " \n" + self.sito + \
               "\n" + str(self.lat) + " \n" + str(self.lng) + " \n" + self.categoria + " \n" + \
               str(self.punt_emoji) + " \n" + str(self.punt_foto) + " \n" + str(self.punt_testo)

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
