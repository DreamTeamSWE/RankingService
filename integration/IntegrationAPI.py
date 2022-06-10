import unittest
import requests


class TestCrawledData(unittest.TestCase):
    def test_get_ranking(self):
        endpoint = 'https://cs0thtwbr7.execute-api.eu-central-1.amazonaws.com/dev/getRanking'
        params = {'size': 5}
        response = requests.get(endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

        self.assertIn('id_ristorante', response.json()[0])
        self.assertIn('nome_ristorante', response.json()[0])
        self.assertIn('indirizzo', response.json()[0])
        self.assertIn('telefono', response.json()[0])
        self.assertIn('sito_web', response.json()[0])
        self.assertIn('latitudine', response.json()[0])
        self.assertIn('longitudine', response.json()[0])
        self.assertIn('categoria', response.json()[0])
        self.assertIn('punteggio_emoji', response.json()[0])
        self.assertIn('punteggio_foto', response.json()[0])
        self.assertIn('punteggio_testo', response.json()[0])

    def test_get_label_and_post(self):
        endpoint = 'https://cs0thtwbr7.execute-api.eu-central-1.amazonaws.com/dev/getLabelAndPost'
        params = {'id_rist': 6}
        response = requests.post(endpoint, json=params)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id_post', response.json()[0])
        self.assertIn('nome_utente', response.json()[0])
        self.assertIn('data_post', response.json()[0])
        self.assertIn('id_ristorante', response.json()[0])
        self.assertIn('testo', response.json()[0])
        self.assertIn('punteggio_emoji', response.json()[0])
        self.assertIn('punteggio_foto', response.json()[0])
        self.assertIn('punteggio_testo', response.json()[0])

    def test_search_by_name(self):
        endpoint = 'https://cs0thtwbr7.execute-api.eu-central-1.amazonaws.com/dev/searchByName'
        name = 'Piazza'
        response = requests.post(endpoint, json={'name': name})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id_ristorante', response.json()[0])
        self.assertIn('nome_ristorante', response.json()[0])
        self.assertIn('indirizzo', response.json()[0])
        self.assertIn('telefono', response.json()[0])
        self.assertIn('sito_web', response.json()[0])
        self.assertIn('latitudine', response.json()[0])
        self.assertIn('longitudine', response.json()[0])
        self.assertIn('categoria', response.json()[0])
        self.assertIn('punteggio_emoji', response.json()[0])
        self.assertIn('punteggio_foto', response.json()[0])
        self.assertIn('punteggio_testo', response.json()[0])

    def test_favorites(self):
        endpoint = 'https://cs0thtwbr7.execute-api.eu-central-1.amazonaws.com/dev/favorites'
        params = {'action': 'add', 'user': '0b48fb2b-a40f-4216-a799-5ed1c3a1a273', 'restaurant': 6}
        response = requests.get(endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

        params = {'action': 'get', 'user': '0b48fb2b-a40f-4216-a799-5ed1c3a1a273'}
        response = requests.get(endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id_ristorante', response.json()[0])
        self.assertIn('nome_ristorante', response.json()[0])

        params = {'action': 'remove', 'user': '0b48fb2b-a40f-4216-a799-5ed1c3a1a273', 'restaurant': 6}
        response = requests.get(endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_general_filter(self):
        endpoint = 'https://cs0thtwbr7.execute-api.eu-central-1.amazonaws.com/dev/generalFilter'
        params = {'radius': 1, 'location': 'Padova', 'size': 1000}
        response = requests.get(endpoint, params=params)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertIn('id_ristorante', response.json()[0])
        self.assertIn('nome_ristorante', response.json()[0])
        self.assertIn('indirizzo', response.json()[0])
        self.assertIn('telefono', response.json()[0])
        self.assertIn('sito_web', response.json()[0])
        self.assertIn('latitudine', response.json()[0])
        self.assertIn('longitudine', response.json()[0])
        self.assertIn('punteggio_emoji', response.json()[0])
        self.assertIn('punteggio_foto', response.json()[0])
        self.assertIn('punteggio_testo', response.json()[0])



if __name__ == '__main__':
    unittest.main()
