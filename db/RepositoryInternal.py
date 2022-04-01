from db.Database import Database
from entity.Restaurant import Restaurant


class RepositoryInternal:
    def __init__(self):
        pass

    def __save_new_restaurant(self, restaurant: Restaurant) -> int:
        query = "INSERT INTO ristorante (" \
                "nome_ristorante, " \
                "indirizzo, " \
                "citta, " \
                "provincia, " \
                "telefono, " \
                "sito_web, " \
                "orario_apertura, " \
                "orario_chiusura, " \
                "latitudine, " \
                "longitudine, " \
                "punteggio_emoji, " \
                "punteggio_foto, " \
                "punteggio_testo) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (restaurant.nome, restaurant.indirizzo, restaurant.citta, restaurant.provincia, restaurant.telefono,
                  restaurant.sito, restaurant.orario_aperture, restaurant.orario_chiusura, restaurant.lat,
                  restaurant.lng,
                  restaurant.punt_emoji, restaurant.punt_foto, restaurant.punt_testo)

        database = Database('ranking_test')
        response = database.do_write_query(query, values)
        return response

    def update_restaurant_info(self, restaurant: Restaurant) -> int:
        query = "UPDATE ristorante SET " \
                "nome_ristorante=%s, " \
                "indirizzo=%s, " \
                "citta=%s, " \
                "provincia=%s, " \
                "telefono=%s, " \
                "sito_web=%s, " \
                "orario_apertura=%s, " \
                "orario_chiusura=%s, " \
                "latitudine=%s, " \
                "longitudine=%s, " \
                "punteggio_emoji=%s, " \
                "punteggio_foto=%s, " \
                "punteggio_testo=%s WHERE id=%s"
        values = (restaurant.nome, restaurant.indirizzo, restaurant.citta, restaurant.provincia, restaurant.telefono,
                  restaurant.sito, restaurant.orario_aperture, restaurant.orario_chiusura, restaurant.lat,
                  restaurant.lng,
                  restaurant.punt_emoji, restaurant.punt_foto, restaurant.punt_testo, restaurant.id_rist)

        database = Database('ranking_test')
        response = database.do_write_query(query, values)
        if response is None:
            response = self.__save_new_restaurant(restaurant)
        return response

    def get_restaurant_info(self, name: str) -> Restaurant:
        query = "SELECT * FROM ristorante WHERE nome_ristorante=%s"
        values = name
        database = Database('ranking_test')
        response = database.do_read_query(query, values)
        if response is not None:
            restaurant = Restaurant(response[0], response[1], response[2], response[3], response[4], response[5],
                                    response[6], response[7], response[8], response[9], response[10], response[11],
                                    response[12], response[13])
            return restaurant

        return Restaurant()
