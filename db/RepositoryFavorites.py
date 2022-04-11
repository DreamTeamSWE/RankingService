from db.DatabaseHandler import DatabaseHandler


class RepositoryFavorites:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    def add_favorite(self, nome_utente: str, id_ristorante: int) -> None:

        param_user_id = {'name': 'nome_utente', 'value': {'stringValue': nome_utente}}
        param_restaurant_id = {'name': 'id_ristorante', 'value': {'longValue': id_ristorante}}
        params = [param_user_id, param_restaurant_id]
        query = 'INSERT INTO preferiti (nome_utente, id_ristorante) VALUES (:nome_utente, :id_ristorante)'
        response = len(self.database.do_write_query(query, params)) > 0
        return response



