from db.DatabaseHandler import DatabaseHandler


class RepositoryFavorites:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    def __add_new_user(self, username: str) -> bool:
        query = 'INSERT INTO utente (nome_utente) VALUES (:nome_utente)'
        response = len(
            self.database.do_write_query(
                query, {'name': 'nome_utente', 'value': {'stringValue': username}}
            )
        ) > 0
        return response

    def __user_exists(self, username: str) -> bool:
        query = 'SELECT * FROM utente WHERE nome_utente = :nome_utente'
        response = len(
            self.database.do_read_query(
                query, {'name': 'nome_utente', 'value': {'stringValue': username}}
            )
        ) > 0
        return response

    def add_favorite(self, username: str, id_restaurant: int) -> bool:
        if self.__user_exists(username):
            print('L\'utente non esiste')
            self.__add_new_user(username)
            print('Aggiunto nuovo utente!')

        param_user_id = {'name': 'nome_utente', 'value': {'stringValue': username}}
        param_restaurant_id = {'name': 'id_ristorante', 'value': {'longValue': id_restaurant}}
        params = [param_user_id, param_restaurant_id]
        query = 'INSERT INTO preferiti (nome_utente, id_ristorante) VALUES (:nome_utente, :id_ristorante)'
        response = len(self.database.do_write_query(query, params)) > 0
        return response

    def remove_favorite(self, username: str, id_restaurant: int) -> bool:
        param_user_id = {'name': 'nome_utente', 'value': {'stringValue': username}}
        param_restaurant_id = {'name': 'id_ristorante', 'value': {'longValue': id_restaurant}}
        params = [param_user_id, param_restaurant_id]
        query = 'DELETE FROM preferiti WHERE nome_utente = :nome_utente AND id_ristorante = :id_ristorante'
        response = len(self.database.do_write_query(query, params)) > 0
        return response

    def get_favorites(self, username: str) -> dict:
        query = 'SELECT * FROM preferiti WHERE nome_utente = :nome_utente'
        response = self.database.do_read_query(
                query, {'name': 'nome_utente', 'value': {'stringValue': username}}
            )
        return response

