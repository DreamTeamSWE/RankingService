import unittest
from db.DatabaseHandler import DatabaseHandler


class TestCrawledData(unittest.TestCase):
    def setUp(self) -> None:
        self.data_base_handelr = DatabaseHandler('ranking_integration')

    def test_select_utente(self):
        query = "SELECT * FROM utente"
        response = self.data_base_handelr.do_read_query(query)
        self.assertEqual(response[0]['nome_utente'], 'user')

    def test_select_label(self):
        query = "SELECT * FROM label"
        response = self.data_base_handelr.do_read_query(query)
        self.assertEqual(response[0]['nome_label'], 'label')

    def test_select_ristorante(self):
        query = "SELECT * FROM ristorante"
        response = self.data_base_handelr.do_read_query(query)
        self.assertEqual(response[0]['id_ristorante'], 1)
        self.assertEqual(response[0]['nome_ristorante'], 'cracco')
        self.assertEqual(response[0]['latitudine'], '10.0000')
        self.assertEqual(response[0]['longitudine'], '20.0000')
        self.assertEqual(response[0]['categoria'], 'italian restaurant')
        self.assertEqual(response[0]['punteggio_emoji'], 1)
        self.assertEqual(response[0]['punteggio_foto'], 1)
        self.assertEqual(response[0]['punteggio_testo'], 1)


if __name__ == '__main__':
    unittest.main()
