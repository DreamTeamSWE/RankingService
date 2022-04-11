from typing import List, Dict

import boto3
import csv
import emoji


class EmojiAnalyser:
    def __init__(self):
        self.__emoji_scores = EmojiAnalyser.__generate_emoji_scores('emoji_ranking.csv')
        self.__weights = {
            'SINGLE_EMOJI': 1,
            'DOUBLE_EMOJI': 2,
            'TRIPLE_EMOJI': 3,
            'MULTIPLE_EMOJI': 4,
            'MULTIPLE_EMOJI_ENDING': 5
        }

    @staticmethod
    def __generate_emoji_scores(filename):
        emoji_sentiment_scores = {}
        s3 = boto3.client(service_name='s3')
        content_object = s3.get_object(Bucket='sweet-emoji-sentiment-scores', Key='emoji_ranking.csv')
        file_content = content_object['Body'].read().decode('utf-8')
        csv_reader = csv.reader(file_content, delimiter=',')
        next(csv_reader)  # salta l'header del file csv
        for line in csv_reader:
            emoji_sentiment_scores[line[0]] = float(line[8])  # nella forma {..., 'emoji': sentiment_value, ...}

        return emoji_sentiment_scores

    @staticmethod
    def __group_repeated_emoji(emoji_list: List[Dict]) -> List[Dict]:
        last_seen_emoji = ''
        last_seen_emoji_counter = 1
        result = []
        for emoji_data in emoji_list:
            if last_seen_emoji != emoji_data['emoji']:
                result.append({'emoji': last_seen_emoji, 'count': last_seen_emoji_counter})
                last_seen_emoji = emoji_data['emoji']
                last_seen_emoji_counter = 1
            else:
                last_seen_emoji_counter += 1

        result.append(
            {'emoji': last_seen_emoji, 'count': last_seen_emoji_counter, 'last_pos': emoji_list[-1]['match_end']})

        return result

    def calculate_score(self, post_text: str) -> float:
        score_x_weight_sum = 0
        weigh_sum = 0

        post_emoji_list = emoji.emoji_list(post_text)

        if len(post_emoji_list) == 0:
            return None

        processed_emoji_list = EmojiAnalyser.__group_repeated_emoji(post_emoji_list)

        for emoji_data in processed_emoji_list:
            if emoji_data['emoji'] in self.__emoji_scores:

                emoji_score = self.__emoji_scores[emoji_data['emoji']]

                if 'last_pos' in emoji_data \
                        and emoji_data['count'] >= 2 \
                        and len(post_text) == emoji_data['last_pos']:
                    score_x_weight_sum += emoji_score * self.__weights['MULTIPLE_EMOJI_ENDING']
                    weigh_sum += self.__weights['MULTIPLE_EMOJI_ENDING']
                elif emoji_data['count'] == 1:
                    score_x_weight_sum += emoji_score * self.__weights['SINGLE_EMOJI']
                    weigh_sum += self.__weights['SINGLE_EMOJI']
                elif emoji_data['count'] == 2:
                    score_x_weight_sum += emoji_score * self.__weights['DOUBLE_EMOJI']
                    weigh_sum += self.__weights['DOUBLE_EMOJI']
                elif emoji_data['count'] == 3:
                    score_x_weight_sum += emoji_score * self.__weights['TRIPLE_EMOJI']
                    weigh_sum += self.__weights['TRIPLE_EMOJI']
                elif emoji_data['count'] >= 4:
                    score_x_weight_sum += emoji_score * self.__weights['MULTIPLE_EMOJI']
                    weigh_sum += self.__weights['MULTIPLE_EMOJI']

        return score_x_weight_sum / weigh_sum
