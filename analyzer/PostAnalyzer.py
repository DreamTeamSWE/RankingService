import boto3
from abc import ABC
from typing import Optional

from analyzer.Analyzer import Analyzer
from analyzer.EmojiAnalyzer import EmojiAnalyzer
from db.RepositoryInternal import RepositoryInternal
from entity import CrawledData
from entity import Image
from entity.ScoreComprehend import ScoreComprehend


class PostAnalyzer(Analyzer, ABC):
    def __init__(self, aws_region='eu-central-1'):
        self.__rekognition = boto3.client(service_name='rekognition', region_name=aws_region)
        self.__comprehend = boto3.client(service_name='comprehend', region_name=aws_region)
        self.__emoji_analyzer = EmojiAnalyzer()
        self.__repository = RepositoryInternal()

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
        print(language)
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

        if language in ['ar', 'hi', 'ko', 'zh-TW', 'ja', 'zh', 'de', 'pt', 'en', 'it', 'fr', 'es']:
            # result of comprehend
            json_result = self.__comprehend.detect_sentiment(Text=post.get_caption(), LanguageCode=language)

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

    def calculate_emoji_score(self, post: CrawledData) -> float:
        emoji_score = self.__emoji_analyzer.analyze(post)
        post.set_emoji_score(emoji_score)
        return emoji_score

    def calculate_text_score(self, post: CrawledData) -> float:
        score = None
        if post.get_caption():
            score = self.__detect_sentiment_text(post, self.__detect_language_text(post.get_caption()))
            post.set_comprehend_score(score)
            post.calculate_and_set_text_score()

        return score

    def calculate_image_score(self, post: CrawledData):
        if not post.get_list_images():
            for image in post.get_list_images():
                image_name = image.get_image_name()
                print("image name " + image_name)
                labels, emotions, emotions_confidence = self.__analyze_image(image_name)

                image.set_labels(labels)
                image.set_emotions(emotions)
                image.set_emotions_confidence(emotions_confidence)
        else:
            print("\nNo image in post\n")

        post.calculate_and_set_image_score()

    def analyze(self, post: CrawledData):
        """
        Analyze a post with Rekognition and Comprehend.
        After analyze, rds db is updated with the new data.

        :param post: Post to analyze
        """
        print("\nHello from PostAnalyzer\n")

        # calcolo punteggio caption con comprehend

        text_score = self.calculate_text_score(post)

        print("\ncomprehend score: " + str(text_score) if text_score else 'no text found' + "\n-------------------\n")

        # calcolo punteggio emoji
        emoji_score = self.calculate_emoji_score(post)

        print('emoji score: ' + str(emoji_score) if emoji_score is not None else 'No emoji detected')

        # calcolo punteggio per ogni immagine e salvo
        self.calculate_image_score(post)
        image_score = post.get_image_score()

        if image_score is not None or text_score is not None:
            self.__repository.save_post(post)
            self.__repository.update_restaurant_scores(post.get_restaurant())
        else:
            print("Post not saved because no meaningful images or text has been found")