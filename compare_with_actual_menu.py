import ujson as json
import cPickle

import load_phrases_and_biz_data
import helpers


def menu_json_to_list_of_menu_items(menu_json):
    menu_json = menu_json.replace("\\\\", "\\")
    menu = json.loads(menu_json)
    menu_items = []
    for sub_menu in menu['sub_menus']:
        for section in sub_menu['sections']:
            for item in section['items']:
                if 'name' in item:
                    item_name = item['name'].lower()
                    menu_items.append(item_name)
    return menu_items

def biz_data_menu_to_menu_items(biz_data_menu):
    return menu_json_to_list_of_menu_items(biz_data_menu['menu'][0]['menu'])


def score_comparison(results, biz_id):
    pass

#score = compare_with_actual_menu(results, biz)
def compare_with_actual_menu(extracted_results, biz):

    extracted_results_dict = {}
    for result in extracted_results:
        extracted_results_dict[result['candidate_menu_item']] = result

    actual_menu_items = biz_data_menu_to_menu_items(a_biz_data)
    sorted_extracted_results = sorted(extracted_result, key=lambda x: x['extraction_score'], reverse=True)
    sorted_extracted_menu_items = map(lambda x:x['candidate_menu_item'], sorted_extracted_results)
    
    matching_items = set(sorted_extracted_menu_items).intersection(set(actual_menu_items))
    extracted_non_matching = set(sorted_extracted_menu_items).difference(set(actual_menu_items))

    extracted_non_matching_with_scores = [(item, extracted_results_dict[item]['extraction_score']) for item in extracted_non_matching]
    extracted_non_matching_with_scores.sort(key=lambda x: x[1], reverse=True)

    
    comparison = {}
    percent_of_menu_found = float(len(matching_items)) /  len(actual_menu_items)
    extra_terms = len(extracted_results) - len(actual_menu_items)
    comparison['percent_of_menu_found'] = percent_of_menu_found
    comparison['extra_terms'] = extra_terms




def print_comparison(a_biz_data, extracted_result):
    extracted_results_dict = {}
    for result in extracted_result:
        extracted_results_dict[result['candidate_menu_item']] = result

    actual_menu_items = biz_data_menu_to_menu_items(a_biz_data)
    sorted_extracted_results = sorted(extracted_result, key=lambda x: x['extraction_score'], reverse=True)
    sorted_extracted_menu_items = map(lambda x:x['candidate_menu_item'], sorted_extracted_results)
    
    matching_items = set(sorted_extracted_menu_items).intersection(set(actual_menu_items))
    extracted_non_matching = set(sorted_extracted_menu_items).difference(set(actual_menu_items))

    print "%s (%s), has %d menu itmes." % (a_biz_data['review'][0]['name'], a_biz_data['review'][0]['id'], len(actual_menu_items))
    print "We got the following menu items correct:"
    for item in matching_items:
        print "\t", item.ljust(20), '\t', extracted_results_dict[item]['extraction_score']

    print "Extracted terms not in the menu:"
    extracted_non_matching_with_scores = [(item, extracted_results_dict[item]['extraction_score']) for item in extracted_non_matching]
    extracted_non_matching_with_scores.sort(key=lambda x: x[1], reverse=True)
    for item in extracted_non_matching_with_scores:
        print "\t", item[0].ljust(20), '\t', item[1]

def load_results(filename, path="../data/"):
    results = cPickle.load(open(path + '/' + filename))

if __name__ == '__main__':
    print "Loading testing data"
    biz_data = load_phrases_and_biz_data.get_biz_data("tri_city_test_biz_id_index_menu_and_review_filtered.json", "../data/")
    results = load_results("results.pkl", "../data")
    sample_id = '12942341'
    some_biz = biz_data[sample_id]
    print "Loading pickled data"
    cPickle.dump(some_biz, open("some_biz.pkl", "w"))
    some_biz = cPickle.load(open("some_biz.pkl"))
    some_result = cPickle.load(open("tmp_results.pkl"))
    print_comparison(some_biz, some_result)
    
