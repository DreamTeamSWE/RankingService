class Restaurant:
    def __init__(self, id_rist: int = None, nome: str = None, indirizzo: str = None, citta: str = None,
                 provincia: str = None, telefono: str = None, sito: str = None,
                 orario_aper: str = None, orario_chiu: str = None, lat: float = None, lng: float = None,
                 punt_emoji: int = None, punt_foto: int = None,
                 punt_testo: int = None) -> None:
        self.id_rist = id_rist
        self.nome = nome
        self.indirizzo = indirizzo
        self.citta = citta
        self.provincia = provincia
        self.telefono = telefono
        self.sito = sito
        self.orario_aperture = orario_aper
        self.orario_chiusura = orario_chiu
        self.lat = lat
        self.lng = lng
        self.punt_emoji = punt_emoji
        self.punt_foto = punt_foto
        self.punt_testo = punt_testo

    def set_punt_emoji(self, punt_emoji: int) -> None:
        self.punt_emoji = punt_emoji

    def set_punt_foto(self, punt_foto: int) -> None:
        self.punt_foto = punt_foto

    def set_punt_testo(self, punt_testo: int) -> None:
        self.punt_testo = punt_testo
