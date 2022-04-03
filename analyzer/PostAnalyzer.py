from abc import ABC
from analyzer.Analyzer import Analyzer
from entity import CrawledData
from entity.ScoreComprehend import ScoreComprehend
import boto3

AWS_REGION = 'eu-central-1'


class PostAnalyzer(Analyzer, ABC):
    def analyze(self, post: CrawledData):
        print("Hello from PostAnalyzer")
        comprehend = boto3.client(service_name='comprehend',
                                  region_name=AWS_REGION)
        # result of comprehend
        json_result = comprehend.detect_sentiment(Text=post.caption, LanguageCode='it')

        print(json_result)

        # get sentiment
        sentiment_score = json_result["Sentiment"]

        array = json_result["SentimentScore"]

        negative = array["Negative"] * 100
        neutral = array["Neutral"] * 100
        positive = array["Positive"] * 100

        # get score
        score = ScoreComprehend(negative, neutral, positive)
        score.set_sentiment(sentiment_score)

        print("\n" + str(score) + "\n-------------------\n")

        # rekognition = boto3.client(service_name='rekognition',
        #                            region_name=AWS_REGION,
        #                            aws_access_key_id=AWS_KEY,
        #                            aws_secret_access_key=AWS_PSW)
