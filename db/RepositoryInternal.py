from db.Database import Database
from entity.Restaurant import Restaurant
from entity.CrawledData import CrawledData


class RepositoryInternal:
    def __init__(self):
        pass

    def __save_new_restaurant(self, restaurant: Restaurant) -> int:
        query = "INSERT INTO ristorante (nome_ristorante, indirizzo, telefono, sito_web, " \
                "latitudine, longitudine, categoria,punteggio_emoji, punteggio_foto, " \
                "punteggio_testo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s %s)"

        values = (restaurant.nome, restaurant.indirizzo, restaurant.telefono, restaurant.sito,
                  restaurant.lat, restaurant.lng, restaurant.categoria, restaurant.punt_emoji, restaurant.punt_foto,
                  restaurant.punt_testo)

        database = Database('ranking_test')
        response = database.do_write_query(query, values)
        return response

    def update_restaurant_info(self, restaurant: Restaurant) -> int:
        query = "UPDATE ristorante SET " \
                "nome_ristorante=%s, " \
                "indirizzo=%s, " \
                "telefono=%s, " \
                "sito_web=%s, " \
                "latitudine=%s, " \
                "longitudine=%s, " \
                "categoria=%s, " \
                "punteggio_emoji=%s, " \
                "punteggio_foto=%s, " \
                "punteggio_testo=%s WHERE id=%s"

        values = (restaurant.nome, restaurant.indirizzo, restaurant.telefono, restaurant.sito,
                  restaurant.lat, restaurant.lng, restaurant.categoria, restaurant.punt_emoji, restaurant.punt_foto,
                  restaurant.punt_testo, restaurant.id_rist)

        database = Database('ranking_test')
        response = database.do_write_query(query, values)
        return response

    def save_post(self, post: CrawledData) -> int:
        query = "INSERT INTO post (nome_utente, data_post, id_ristorante, testo, punteggio_emoji, " \
                "sentiment_comprehend, negative_comprehend, positive_comprehend, neutral_comprehend)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = (post.utente, post.data_post, post.restaurant.id_rist, post.caption, post.punt_emoji,
                  post.score.sentiment_comprehend,
                  post.score.negative_comprehend, post.score.positive_comprehend, post.score.neutral_comprehend)

        database = Database('ranking_test')
        response = database.do_write_query(query, values)
        return response

    # !!! stesso codice di RepositoryExternal.py !!! #
    def get_restaurant_info_by_id(self, id_restaurant: int) -> Restaurant:
        query = "SELECT * FROM ristorante WHERE id_ristorante=%s"
        values = id_restaurant
        database = Database('ranking_test')
        response = database.do_read_query(query, values)
        if response is not None:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return Restaurant()

    def get_restaurant_info_by_name(self, name: str) -> Restaurant:
        query = "SELECT * FROM ristorante WHERE nome_ristorante LIKE '%s%'"
        values = name
        database = Database('ranking_test')
        response = database.do_read_query(query, values)
        if response is not None:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return Restaurant()
