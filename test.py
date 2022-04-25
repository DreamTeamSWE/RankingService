from analyzer.PostAnalyzer import PostAnalyzer

from db.DatabaseHandler import DatabaseHandler
from db.RepositoryInternal import RepositoryInternal
import uuid

from entity.CrawledData import CrawledData
from analyzer.EmojiAnalyzer import EmojiAnalyzer


# event = {"username": "giovanni.fit", "post_id": "2630072851064980714_3478737643", "date": "2021-07-31 16:32:17", "img_url": [3440, 3441, 3442], "caption_text": "Milanese nightlife.\n#meandmywife #mixology #nottinghamforest #dariocomini #milano #firsttruelove #vidaloca", "location": {"location_name": "Nottingham Forest Milano-cocktail bar", "lat": 45.4688, "lng": 9.207, "category": "Cocktail Bar", "phone": "", "website": "http://www.nottingham-forest.com/", "db_id": 1082}}


def main():
    # rint = RepositoryInternal()
    # a = PostAnalyzer()
    # post = CrawledData.parse_post_from_sqs(event)
    # a.analyze(post)
    ea = EmojiAnalyzer()
    print(ea.calculate_score('Nineties cyber ravers. Maximalist hair. Statement knitwear. Hyper reality. 🔥'))


if __name__ == '__main__':
    main()
