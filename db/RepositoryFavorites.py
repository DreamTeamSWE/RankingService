from typing import List
from db.DatabaseHandler import DatabaseHandler


class RepositoryFavorites:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    def __add_new_user(self, username: str) -> bool:
        """
        Add a new user to the database
        :param username: the username of the new user
        :return: True if the user has been added, False otherwise
        """
        query = 'INSERT INTO utente (nome_utente) VALUES (:nome_utente)'
        response = len(
            self.database.do_write_query(
                query, [{'name': 'nome_utente', 'value': {'stringValue': username}}]
            )
        ) > 0
        return response

    def __user_exists(self, username: str) -> bool:
        """
        Check if a user exists in the database  by its username
        :param username: the username of the user
        :return: True if the user exists, False otherwise
        """
        query = 'SELECT * FROM utente WHERE nome_utente = :nome_utente'
        response = len(
            self.database.do_read_query(
                query, [{'name': 'nome_utente', 'value': {'stringValue': username}}]
            )
        ) > 0
        return response

    def add_favorite(self, username: str, id_restaurant: int) -> bool:
        """
        Add a new favorite to the database
        :param username: the username of the user
        :param id_restaurant: the id of the restaurant
        :return: True if the favorite has been added, False otherwise
        """
        if not self.__user_exists(username):
            print('L\'utente non esiste')
            self.__add_new_user(username)
            print('Aggiunto nuovo utente!')

        param_user_id = {'name': 'nome_utente', 'value': {'stringValue': username}}
        param_restaurant_id = {'name': 'id_ristorante', 'value': {'longValue': id_restaurant}}
        params = [param_user_id, param_restaurant_id]
        query = 'INSERT IGNORE INTO preferito (nome_utente, id_ristorante) VALUES (:nome_utente, :id_ristorante)'
        response = len(self.database.do_write_query(query, params)) > 0
        return response

    def remove_favorite(self, username: str, id_restaurant: int) -> bool:
        """
        Remove a favorite from the database by its id
        :param username: the username of the user
        :param id_restaurant: the id of the restaurant
        :return: True if the favorite has been removed, False otherwise
        """
        param_user_id = {'name': 'nome_utente', 'value': {'stringValue': username}}
        param_restaurant_id = {'name': 'id_ristorante', 'value': {'longValue': id_restaurant}}
        params = [param_user_id, param_restaurant_id]
        query = 'DELETE FROM preferito WHERE nome_utente = :nome_utente AND id_ristorante = :id_ristorante'
        response = self.database.do_write_query(query, params)
        return response['numberOfRecordsUpdated'] > 0

    def get_favorites(self, username: str) -> dict:
        """
        Get all the favorites of a user by its username
        :param username: the username of the user
        :return: a list of all the favorites of the user (name of the restaurants and their ids)
        or an empty list if the user does not exist
        """
        query = 'select ristorante.id_ristorante, ristorante.nome_ristorante from preferito join ristorante on ' \
                'ristorante.id_ristorante = preferito.id_ristorante WHERE ' \
                'preferito.nome_utente = :nome_utente '
        response = self.database.do_read_query(
            query, [{'name': 'nome_utente', 'value': {'stringValue': username}}]
        )
        return response
