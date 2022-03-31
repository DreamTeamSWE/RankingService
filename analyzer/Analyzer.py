from abc import ABC, abstractmethod
from entity import CrawledData


class Analyzer(ABC):

    @abstractmethod
    def postanalyzer(self, post: CrawledData):
        pass
