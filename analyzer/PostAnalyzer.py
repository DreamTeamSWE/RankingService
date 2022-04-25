import boto3
from abc import ABC
from analyzer.Analyzer import Analyzer
from analyzer.EmojiAnalyzer import EmojiAnalyzer
from entity import CrawledData
from entity import Image
from entity.ScoreComprehend import ScoreComprehend
from db.RepositoryInternal import RepositoryInternal

__AWS_REGION = 'eu-central-1'


def detect_language_text(text: str) -> str:
    # TODO: testare perché fatto in automatico con copilot
    """
    Detect language of a text with Translate.

    :param text: text to analyze with Translate

    :rtype: str
    :return: language of the text
    """
    print("\n-------------------")
    print('detect_language_text')

    translate = boto3.client(service_name='translate',
                             region_name=__AWS_REGION)
    # result of translate
    json_result = translate.detect_language(Text=text)

    # get language
    language = json_result["LanguageCode"]

    return language


def detect_sentiment_text(post: CrawledData, language: str = 'it') -> ScoreComprehend:
    """
    Detect sentiment of a post with Comprehend.

    :param post: post to analyze with Comprehend
    :param language: laungage of the caption

    :rtype: ScoreComprehend
    :return: Comprehend confidence score
    """
    print("\n-------------------")
    print('detect_sentiment_text')

    comprehend = boto3.client(service_name='comprehend',
                              region_name=__AWS_REGION)
    # result of comprehend
    json_result = comprehend.detect_sentiment(Text=post.caption, LanguageCode=language)

    # get sentiment
    array = json_result["SentimentScore"]
    principal_sentiment = json_result["Sentiment"]

    MULT_FACTOR = 100

    # get score
    negative = int(array["Negative"] * MULT_FACTOR)
    neutral = int(array["Neutral"] * MULT_FACTOR)
    positive = int(array["Positive"] * MULT_FACTOR)
    mixed = int(array["Mixed"] * MULT_FACTOR)

    score = ScoreComprehend(negative, positive, neutral, mixed)
    score.set_sentiment(principal_sentiment)

    return score


def detect_labels(photo: Image, bucket: str):
    """
    Detect object of an image with Rekognition.

    :param bucket: name of S3 bucket
    :param photo: image to analyze with Rekognition

    :rtype: dict, bool
    :return: Dictionary of labels and boolean if there is a person
    """
    print("\n-------------------")
    print('detect_labels')

    client = boto3.client('rekognition', region_name=__AWS_REGION)

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
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


def detect_sentiment_person(name_image: str, bucket: str):
    """
    Detect sentiment of a person with Comprehend.

    :param name_image: name of the image to analyze with Rekognition
    :param bucket: name of S3 bucket

    :rtype: dict, bool
    :return: Dictionary of emotions and boolean if emotions were found
    """
    print("\n-------------------")
    print('detect_sentiment_person')

    reko = boto3.client('rekognition', region_name=__AWS_REGION)
    print(name_image)
    response = reko.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': name_image}},
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


def image_analyzer(name_image: str):
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

    labels, contain_person = detect_labels(name_image, bucket)
    if contain_person:
        print("There is a person")

        emotions, contain_emotion, emotions_confidence = detect_sentiment_person(name_image, bucket)
        if not contain_emotion:
            print("Emotion detected")
        else:
            print("No emotion detected")
    else:
        print("There is no person")

    print("-------------------\n")
    return labels, emotions, emotions_confidence


def emoji_analyzer(post_text: str):
    ea = EmojiAnalyzer()
    return ea.calculate_score(post_text)

class PostAnalyzer(Analyzer, ABC):
    def analyze(self, post: CrawledData):
        """
        Analyze a post with Rekognition and Comprehend.
        After analyze, rds db is updated with the new data.

        :param post: Post to analyze
        """
        print("\nHello from PostAnalyzer\n")

        # calcolo punteggio caption con comprehend
        score = detect_sentiment_text(post)
        post.set_punt_testo(score)

        print("\ncomprehend score: " + str(score) + "\n-------------------\n")

        # calcolo punteggio emoji
        emoji_score = emoji_analyzer(post.caption)
        post.set_punt_emoji(emoji_score)

        print('emoji score: ' + str(emoji_score) if emoji_score is not None else 'No emoji detected')

        # calcolo punteggio per ogni immagine e salvo
        if post.list_images is not None:
            for image in post.list_images:
                print("image name " + image.image_name)
                labels, emotions, emotions_confidence = image_analyzer(image.image_name)

                image.set_labels(labels)
                image.set_emotions(emotions)
                image.set_emotions_confidence(emotions_confidence)

        else:
            print("\nNo image in post\n")

        post.calculate_and_set_punt_foto()
        repository = RepositoryInternal()
        repository.save_post(post)
