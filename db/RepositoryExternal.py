from db.Database import Database
from entity.Filter import Filter
from entity.Restaurant import Restaurant


class RepositoryExternal:
    def __init__(self):
        self.database = Database('ranking_test')

    def get_ranking(self, filter_from_front: Filter) -> list:
        query = "SELECT * FROM ristorante WHERE %s"
        values = (filter_from_front.make_query())
        parsed_records = self.database.do_read_query(query, values)
        return parsed_records

    # !!! stesso codice di RepositoryInternal.py !!! #
    def get_restaurant_info(self, name: str) -> Restaurant:
        query = "SELECT * FROM ristorante WHERE nome_ristorante=%s"
        values = name
        response = self.database.do_read_query(query, values)
        if response is not None:
            restaurant = Restaurant(response[0], response[1], response[2], response[3], response[4], response[5],
                                    response[6], response[7], response[8], response[9], response[10], response[11],
                                    response[12], response[13])
            return restaurant

        return Restaurant()
