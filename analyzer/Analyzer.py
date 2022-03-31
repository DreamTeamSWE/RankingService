from abc import ABC, abstractmethod
from entity import CrawledData


class Analyzer(ABC):

    @abstractmethod
    def analyze(self, post: CrawledData):
        pass
