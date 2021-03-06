from abc import ABC
from typing import List, Dict, Optional

import emoji
import boto3

from analyzer.Analyzer import Analyzer
from entity.CrawledData import CrawledData


class EmojiAnalyzer(Analyzer, ABC):
    def __init__(self):
        self.__emoji_scores = EmojiAnalyzer.__generate_emoji_scores('emoji_ranking_normalized_1.csv')
        self.weights = {
            'SINGLE_EMOJI': 1,
            'DOUBLE_EMOJI': 2,
            'TRIPLE_EMOJI': 3,
            'MULTIPLE_EMOJI': 4,
            'MULTIPLE_EMOJI_ENDING': 1.3,
            'SINGLE_EMOJI_ENDING': 1.2
        }

    @staticmethod
    def __generate_emoji_scores(filename: str):
        result = {}
        s3 = boto3.client(service_name='s3')
        content_object = s3.get_object(Bucket='sweet-emoji-sentiment-scores', Key=filename)
        file_content = content_object['Body'].read().decode('utf-8')
        lines = file_content.split("\n")
        for line in lines:
            values = line.split(",")
            if len(values) == 12:
                result[values[0]] = float(values[8])
        return result

    @staticmethod
    def __group_repeated_emoji(emoji_list: List[Dict]) -> List[Dict]:
        last_seen_emoji = emoji_list[0]['emoji']
        last_seen_emoji_counter = 0
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

    def analyze(self, post: CrawledData) -> Optional[float]:
        score_x_weight_sum = 0.0
        weigh_sum = 0.0
        post_text = post.get_caption()
        extracted_emoji_list = emoji.emoji_list(post_text)
        num_emoji_extracted = len(extracted_emoji_list)
        print(f'extracted {num_emoji_extracted} emoji')
        if num_emoji_extracted > 0:
            processed_emoji_list = EmojiAnalyzer.__group_repeated_emoji(extracted_emoji_list)
            unsupported_emojis = 0

            for emoji_data in processed_emoji_list:
                if emoji_data['emoji'] in self.__emoji_scores:
                    emoji_score = self.__emoji_scores[emoji_data['emoji']]
                    if 'last_pos' in emoji_data \
                            and emoji_data['count'] >= 2 \
                            and len(post_text) == emoji_data['last_pos']:
                        mult_factor = emoji_data['count'] if emoji_data['count'] <= 4 else 4
                        score_x_weight_sum += emoji_score * \
                                              self.weights['MULTIPLE_EMOJI_ENDING'] * mult_factor
                    elif 'last_pos' in emoji_data \
                            and emoji_data['count'] == 1 \
                            and len(post_text) == emoji_data['last_pos']:
                        score_x_weight_sum += emoji_score * self.weights['SINGLE_EMOJI_ENDING']
                    elif emoji_data['count'] == 1:
                        score_x_weight_sum += emoji_score * self.weights['SINGLE_EMOJI']
                    elif emoji_data['count'] == 2:
                        score_x_weight_sum += emoji_score * self.weights['DOUBLE_EMOJI']
                    elif emoji_data['count'] == 3:
                        score_x_weight_sum += emoji_score * self.weights['TRIPLE_EMOJI']
                    elif emoji_data['count'] >= 4:
                        score_x_weight_sum += emoji_score * self.weights['MULTIPLE_EMOJI']

                    weigh_sum += emoji_data['count'] if emoji_data['count'] <= 4 else 4
                else:
                    print('found unsupported emoji')
                    unsupported_emojis += 1

            if weigh_sum > 0.5:  # il minimo pu?? essere 1, 0 significa che non ha trovato niente
                final_score = 100 * score_x_weight_sum / weigh_sum
                return final_score if final_score <= 100 else 100
            else:
                print('found only unsupported emojis')
                return None  # trovato solo emoji non supportate
        else:
            print('found no emoji')
            return None  # non so state trovato emoji

