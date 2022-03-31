from abc import ABC
from entity import CrawledData
from analyzer.Analyzer import Analyzer
import json
from entity.ScoreComprehend import ScoreComprehend
import boto3
import requests

AWS_KEY = 'AKIARZPP2F6HY7YUZJ56'
AWS_PSW = 'YhYNvCJYS8d3EkmsfzK04wQKcNZxw5kO/aJim60F'
AWS_REGION = 'eu-central-1'


class PostAnalyzer(Analyzer, ABC):
    @staticmethod
    def post_analyzer(post: CrawledData):
        print("Hello from PostAnalyzer")
        comprehend = boto3.client(service_name='comprehend',
                                  region_name=AWS_REGION,
                                  aws_access_key_id=AWS_KEY,
                                  aws_secret_access_key=AWS_PSW)

        rekognition = boto3.client(service_name='rekognition',
                                   region_name=AWS_REGION,
                                   aws_access_key_id=AWS_KEY,
                                   aws_secret_access_key=AWS_PSW)

        # result of comprehend
        raw_json = comprehend.detect_sentiment(Text=post.text, LanguageCode='it')

        json_result = json.loads(raw_json)

        print(raw_json)

        # get sentiment
        sentiment_score = json_result["Sentiment"]

        array = json_result["SentimentScore"]

        negative = array["Negative"] * 100
        neutral = array["Neutral"] * 100
        positive = array["Positive"] * 100

        # get score
        score = ScoreComprehend(negative, neutral, positive)
        score.set_sentiment(sentiment_score)

        print("\n" + str(score))


        #
        # source_bytes = requests.get(post.imgURL).content
        # # result of rekognition
        # jsonImgResult = json.dumps(
        #     rekognition.detect_labels(
        #         Image={'Bytes': source_bytes},
        #         MaxLabels=100),
        #     indent=4)
        # print(jsonImgResult)
