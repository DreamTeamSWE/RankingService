from db.DatabaseHandler import DatabaseHandler
from entity.Filter import Filter
from entity.Restaurant import Restaurant


class RepositoryExternal:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    """
    - API che ritorna i tipi di cucina data una ricerca
    - API che ritorna le zone
    - API che ritorna dei locali alternativi, nel caso non ci fosse un risultato “perfetto”
    - API per la gestione dei preferiti, nel caso l’utente sia loggato
    """

    def get_ranking(self, position: int, size: int):
        """
        return restaurants ranking, ordered by sum of punteggio_emoji, punteggio_foto ,punteggio_testo

        :param position: position from where to start (possible numbers start from 0)
        :param size: numbers of restaurants to return
        :return: restaurants ranking
        """

        position_param = {"name": "position", "value": {"longValue": position}}
        size_param = {"name": "size", "value": {"longValue": size}}

        query = "SELECT * FROM ristorante ORDER BY (punteggio_emoji+punteggio_foto+punteggio_testo) DESC LIMIT " \
                ":position, :size"
        response = self.database.do_read_query(query, [position_param, size_param])

        return response

    def get_post_and_tag_by_restaurant(self, id_rist: int):
        """
        return post and tag of restaurant

        :param id_rist: id of restaurant
        :return: post and tag of restaurant
        """
        query = "select * from post p join immagine i on p.id_post = i.id_post join label_img l on l.id_immagine = " \
                "i.id_immagine where p.id_ristorante = :id_ristorante group by p.id_ristorante"

        param = [{"name": "id_ristorante", "value": {"longValue": id_rist}}]

        return self.database.do_read_query(query, param)

        # # !!! stesso codice di RepositoryInternal.py !!! # def get_restaurant_info_by_id(self, id_restaurant: int) ->
    # Restaurant: query = "SELECT * FROM ristorante WHERE id_ristorante=%s" values = id_restaurant response =
    # self.database.do_read_query(query, values) if response is not None: restaurant = Restaurant(id_rist=response[
    # 0], nome=response[1], indirizzo=response[2], telefono=response[3], sito=response[4], lat=response[5],
    # lng=response[6], categoria=response[7], punt_emoji=response[8], punt_foto=response[9], punt_testo=response[10])
    # return restaurant
    #
    #     return Restaurant()
