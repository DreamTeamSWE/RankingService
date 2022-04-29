import boto3
from abc import ABC
from typing import Optional

from analyzer.Analyzer import Analyzer
from analyzer.EmojiAnalyzer import EmojiAnalyzer
from db.RepositoryInternal import RepositoryInternal
from entity import CrawledData
from entity import Image
from entity.ScoreComprehend import ScoreComprehend

__AWS_REGION = 'eu-central-1'


class PostAnalyzer(Analyzer, ABC):
    def __init__(self, aws_region='eu-central-1'):
        self.__rekognition = boto3.client(service_name='rekognition', region_name=aws_region)
        self.__comprehend = boto3.client(service_name='comprehend', region_name=aws_region)
        self.__emoji_analyzer = EmojiAnalyzer()

    def __detect_language_text(self, text: str) -> str:
        """
        Detect language of a text with Comprehend.

        :param text: text to analyze with Comprehend

        :rtype: str
        :return: language of the text
        """
        print("\n-------------------")
        print('detect_language_text')

        # result of comprehend
        json_result = self.__comprehend.detect_dominant_language(Text=text)

        # get first language
        languages = json_result['Languages'][0]

        # get language code
        language = languages['LanguageCode']

        return language

    def __detect_sentiment_text(self, post: CrawledData, language: str = 'it') -> Optional[ScoreComprehend]:
        """
        Detect sentiment of a post with Comprehend.

        :param post: post to analyze with Comprehend
        :param language: laungage of the caption

        :rtype: ScoreComprehend
        :return: Comprehend confidence score
        """
        print("\n-------------------")
        print('detect_sentiment_text')

        if post.get_caption() is not None:
            # result of comprehend
            json_result = self.__comprehend.detect_sentiment(Text=post.get_caption, LanguageCode=language)

            # get sentiment
            array = json_result["SentimentScore"]
            principal_sentiment = json_result["Sentiment"]

            mult_factor = 100

            # get score
            negative = int(array["Negative"] * mult_factor)
            neutral = int(array["Neutral"] * mult_factor)
            positive = int(array["Positive"] * mult_factor)
            mixed = int(array["Mixed"] * mult_factor)

            score = ScoreComprehend(negative, positive, neutral, mixed)
            score.set_sentiment(principal_sentiment)

            return score
        else:
            # no text
            return None

    def __detect_labels(self, photo: Image, bucket: str):
        """
        Detect object of an image with Rekognition.

        :param bucket: name of S3 bucket
        :param photo: image to analyze with Rekognition

        :rtype: dict, bool
        :return: Dictionary of labels and boolean if there is a person
        """
        print("\n-------------------")
        print('detect_labels')

        response = self.__rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                                    MaxLabels=10)
        print('Detecting labels for ' + photo)

        labels_dict = {}
        contain_person = False

        for label in response['Labels']:
            if label['Confidence'] >= 90:
                if label['Name'] == 'Person':
                    contain_person = True
                else:
                    for parent in label['Parents']:
                        if parent['Name'] == 'Food':
                            if label['Name'] in labels_dict:
                                labels_dict[label['Name']] += 1
                            else:
                                labels_dict[label['Name']] = 1
        return labels_dict, contain_person

    def __detect_sentiment_person(self, name_image: str, bucket: str):
        """
        Detect sentiment of a person with Rekognition.

        :param name_image: name of the image to analyze with Rekognition
        :param bucket: name of S3 bucket

        :rtype: dict, bool
        :return: Dictionary of emotions and boolean if emotions were found
        """
        print("\n-------------------")
        print('detect_sentiment_person')

        print(name_image)

        response = self.__rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': name_image}},
                                                   Attributes=['ALL'])
        contain_emotion = True
        emotions_dict = {}
        emotions_confid = []

        for faceDetail in response['FaceDetails']:
            emotions = faceDetail['Emotions']
            confid_single_face = {}
            for emotion in emotions:
                emotion_name = emotion['Type']
                emotion_confid_value = emotion['Confidence']
                if emotion_name != 'UNKNOWN':
                    confid_single_face[emotion_name] = emotion_confid_value

                    if emotion_confid_value >= 90:
                        if emotion_name in emotions_dict:
                            emotions_dict[emotion_name] += 1
                        else:
                            emotions_dict[emotion_name] = 1
                        contain_emotion = False
            emotions_confid.append(confid_single_face)
        return emotions_dict, contain_emotion, emotions_confid

    def __analyze_image(self, name_image: str):
        """
        Analyze an image with Rekognition.

        :param name_image: name of the image to analyze

        :rtype: dict, dict
        :return: Dictionary of labels and dictionary of emotions
        """
        print("\n-------------------")
        print("image_analyzer ")

        bucket = 'dream-team-img-test'
        emotions = {}
        emotions_confidence = {}

        print("\n-------------------")
        print(name_image)

        labels, contain_person = self.__detect_labels(name_image, bucket)
        if contain_person:
            print("There is a person")

            emotions, contain_emotion, emotions_confidence = self.__detect_sentiment_person(name_image, bucket)
            if not contain_emotion:
                print("Emotion detected")
            else:
                print("No emotion detected")
        else:
            print("There is no person")

        print("-------------------\n")
        return labels, emotions, emotions_confidence

    def __analyze_emoji(self, post_text: str) -> float:
        return self.__emoji_analyzer.calculate_score(post_text)

    def analyze(self, post: CrawledData):
        """
        Analyze a post with Rekognition and Comprehend.
        After analyze, rds db is updated with the new data.

        :param post: Post to analyze
        """
        print("\nHello from PostAnalyzer\n")

        # calcolo punteggio caption con comprehend
        score = self.__detect_sentiment_text(post, self.__detect_language_text(post.get_caption))
        post.set_comprehend_score(score)
        post.calculate_and_set_text_score()

        print("\ncomprehend score: " + str(score) if score else 'no text found' + "\n-------------------\n")

        # calcolo punteggio emoji
        emoji_score = self.__analyze_emoji(post.get_caption)
        post.set_emoji_score(emoji_score)

        print('emoji score: ' + str(emoji_score) if emoji_score is not None else 'No emoji detected')

        # calcolo punteggio per ogni immagine e salvo
        if post.get_list_images() is not None:
            for image in post.get_list_images():
                print("image name " + image.image_name)
                labels, emotions, emotions_confidence = self.__analyze_image(image.image_name)

                image.set_labels(labels)
                image.set_emotions(emotions)
                image.set_emotions_confidence(emotions_confidence)

        else:
            print("\nNo image in post\n")

        post.calculate_and_set_image_score()
        repository = RepositoryInternal()
        repository.save_post(post)
        repository.update_restaurant_scores(post.restaurant)
