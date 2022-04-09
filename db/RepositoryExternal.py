from db.Database import Database
from entity.Filter import Filter
from entity.Restaurant import Restaurant


class RepositoryExternal:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = Database(db_name)

    def get_ranking(self, filter_from_front: Filter) -> list:
        query = "SELECT * FROM ristorante WHERE %s"
        values = (filter_from_front.make_query())
        parsed_records = self.database.do_read_query(query, values)
        return parsed_records

    # !!! stesso codice di RepositoryInternal.py !!! #
    def get_restaurant_info_by_id(self, id_restaurant: int) -> Restaurant:
        query = "SELECT * FROM ristorante WHERE id_ristorante=%s"
        values = id_restaurant
        response = self.database.do_read_query(query, values)
        if response is not None:
            restaurant = Restaurant(id_rist=response[0], nome=response[1], indirizzo=response[2], telefono=response[3],
                                    sito=response[4], lat=response[5], lng=response[6], categoria=response[7],
                                    punt_emoji=response[8],
                                    punt_foto=response[9], punt_testo=response[10])
            return restaurant

        return Restaurant()
