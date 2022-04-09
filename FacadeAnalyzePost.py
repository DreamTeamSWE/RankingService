from analyzer import Analyzer
from entity.CrawledData import CrawledData
from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(post: CrawledData, analyzer: Analyzer, repository: RepositoryInternal):
    analyzer.analyze(post=post)
    restaurant = repository.get_restaurant_info_by_id(post.restaurant.id_rist)
    repository.update_restaurant_info(restaurant)


class FacadeAnalyzePost:
    pass
