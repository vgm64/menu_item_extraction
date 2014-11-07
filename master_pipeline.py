
import load_phrases_and_biz_data
import ExtractMenuUsingPhrases

import ujson as json

PATH = '../data/'

BIZ_DATA_FILENAME='biz_id_index_menu_and_review.json'
PREFIX_FILENAME='prefix_support'
SUFFIX_FILENAME='suffix_support'


def master_pipeline():

    prefix_data, suffix_data = load_phrases_and_biz_data.get_phrases(PREFIX_FILENAME, SUFFIX_FILENAME, PATH)
    biz_data = load_phrases_and_biz_data.get_biz_data(BIZ_DATA_FILENAME, PATH)

    for biz_id in biz_data:
        mini_pipeline(biz_data[biz_id], prefix_data, suffix_data)

def mini_pipeline(biz, prefix_data, suffix_data):

    tokens = generate_tokenized_reviews(biz)

    len_of_menu_items = 2
    prefix_results = ExtractMenuUsingPhrases.ExtractMenuItemUsingPrefixPhrases(tokens, prefix_data, len_of_menu_items)
    suffix_results = ExtractMenuUsingPhrases.ExtractMenuItemUsingSuffixPhrases(tokens, suffix_data, len_of_menu_items)

    score = compare_with_actual_menu(results, biz)




