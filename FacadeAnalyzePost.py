from analyzer import Analyzer
from db.RepositoryInternal import RepositoryInternal


def refreshranking(crawlertail, analyzer: Analyzer, repository: RepositoryInternal):
    analyzer.analyze(crawlertail)
    repository.refresh_ranking(analyzer.getranking())


class FacadeAnalyzePost:
    pass
