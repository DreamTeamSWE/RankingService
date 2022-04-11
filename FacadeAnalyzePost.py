from analyzer import Analyzer
from entity.CrawledData import CrawledData
from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(post: CrawledData, analyzer: Analyzer, repository: RepositoryInternal):
    """
    Refresh ranking

    :param post: post to analyze
    :param analyzer: algorithm to use to analyze post
    :param repository: repository to use to store analyzed data
    """
    analyzer.analyze(post=post)
    restaurant = repository.get_restaurant_info_by_id(post.restaurant.id_rist)
    repository.update_restaurant_info(restaurant)


class FacadeAnalyzePost:
    pass
