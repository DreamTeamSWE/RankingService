from analyzer import Analyzer
from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(crawler_tail, analyzer: Analyzer, repository: RepositoryInternal):
    analyzer.analyze(crawler_tail)
    repository.refresh_ranking(analyzer.getranking())


class FacadeAnalyzePost:
    pass
