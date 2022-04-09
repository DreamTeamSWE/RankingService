class Restaurant:
    def __init__(self, id_rist: int = None, nome: str = None, indirizzo: str = None, telefono: str = None,
                 sito: str = None, lat: float = None, lng: float = None, categoria: str = None,
                 punt_emoji: int = None, punt_foto: int = None,
                 punt_testo: int = None) -> None:
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
