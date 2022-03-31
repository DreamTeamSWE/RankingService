from analyzer import Analyzer
from entity.CrawledData import CrawledData


# from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(post: CrawledData, analyzer: Analyzer, repository):
    analyzer.analyze(post=post)
    # repository.refresh_ranking(analyzer.getranking())


class FacadeAnalyzePost:
    pass
