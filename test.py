from analyzer.PostAnalyzer import PostAnalyzer

from db.DatabaseHandler import DatabaseHandler
from db.RepositoryFavorites import RepositoryFavorites
from db.RepositoryInternal import RepositoryInternal
import uuid
import random

from entity.CrawledData import CrawledData
from analyzer.EmojiAnalyzer import EmojiAnalyzer


# event = {"username": "giovanni.fit", "post_id": "2630072851064980714_3478737643", "date": "2021-07-31 16:32:17", "img_url": [3440, 3441, 3442], "caption_text": "Milanese nightlife.\n#meandmywife #mixology #nottinghamforest #dariocomini #milano #firsttruelove #vidaloca", "location": {"location_name": "Nottingham Forest Milano-cocktail bar", "lat": 45.4688, "lng": 9.207, "category": "Cocktail Bar", "phone": "", "website": "http://www.nottingham-forest.com/", "db_id": 1082}}


def main():
    ristoranti_disponibili = [8, 43, 57, 58, 59, 61, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76]
    for i in range(10):
        idutente = str(uuid.uuid4())
        random_len = random.randint(5, 18)
        rist_pref = random.sample(ristoranti_disponibili, random_len)
        rf = RepositoryFavorites()
        print(idutente)
        print(rist_pref)
        print('-------------------------')
        for rist in rist_pref:
            rf.add_favorite(idutente, rist)
    # rint = RepositoryInternal()
    # a = PostAnalyzer()
    # post = CrawledData.parse_post_from_sqs(event)
    # a.analyze(post)
    #ea = EmojiAnalyzer()
    #print(ea.calculate_score('Espetacular a qualidade dos peixes 👏🏻👏🏻👏🏻 com uma gastronomia asiática maravilhosa RECOMENDO !!!@kazuoharada @kazuo.restaurante @estiloramy'))


if __name__ == '__main__':
    main()
