import load_phrases_and_biz_data
import ExtractMenuUsingPhrases
#helpers is a file that defines some helper functions for counting dictionaries
import helpers
import generateTokenizedRevs
import get_candidate_menu_items
from operator import itemgetter
import DictLookUp

import ujson as json

PATH = '/scratch/mariachr/menu_item_extraction/data/'

BIZ_DATA_FILENAME='tri_city_test_biz_id_index_menu_and_review_filtered.json'
PREFIX_FILENAME='prefix_support_train'
SUFFIX_FILENAME='suffix_support_train'
MENU_DICT_FILENAME='menudict_train.p'
MENU_ITEM_LENGTH = 2

def load_data_only():
	prefix_data, suffix_data = load_phrases_and_biz_data.get_phrases(PREFIX_FILENAME, SUFFIX_FILENAME, PATH)
	biz_data = load_phrases_and_biz_data.get_biz_data(BIZ_DATA_FILENAME, PATH)
	menu_dict = DictLookUp.load_menu_dictionary(PATH,MENU_DICT_FILENAME)
	return prefix_data,suffix_data,biz_data,menu_dict

def get_candidates(biz,prefix_data,suffix_data):
	tokens = generateTokenizedRevs.GenerateTokenizedRevs(biz)

        candidate_menu_items_by_prefix = get_candidate_menu_items.extract_candidate_menu_items_from_prefix(tokens, prefix_data, MENU_ITEM_LENGTH)
        candidate_menu_items_by_suffix = get_candidate_menu_items.extract_candidate_menu_items_from_suffix(tokens, suffix_data, MENU_ITEM_LENGTH)
	return candidate_menu_items_by_prefix,candidate_menu_items_by_suffix

def master_pipeline():
	
	print "LOADING DATA..."
	menu_dict = DictLookUp.load_menu_dictionary(PATH,MENU_DICT_FILENAME)
	prefix_data, suffix_data = load_phrases_and_biz_data.get_phrases(PREFIX_FILENAME, SUFFIX_FILENAME, PATH)
 	biz_data = load_phrases_and_biz_data.get_biz_data(BIZ_DATA_FILENAME, PATH)
	
	print "COMPUTING CANDIDATES..."
	fewbizids = get_bizids_with_lots_reviews(biz_data,5)
	for biz_id,nreviews in fewbizids:
		print "FOR BUSINESS: %s" % biz_id
		print "Name: %s" % biz_data[biz_id]['review'][0]['name']
		print "Number of Reviews: %s" % nreviews
		mini_pipeline(biz_data[biz_id], prefix_data, suffix_data,menu_dict)

def mini_pipeline(biz, prefix_data, suffix_data,menudict):

	tokens = generateTokenizedRevs.GenerateTokenizedRevs(biz)
	#print tokens
	candidate_menu_items_by_prefix = get_candidate_menu_items.extract_candidate_menu_items_from_prefix(tokens, prefix_data, MENU_ITEM_LENGTH)
	candidate_menu_items_by_suffix = get_candidate_menu_items.extract_candidate_menu_items_from_suffix(tokens, suffix_data, MENU_ITEM_LENGTH)
	
	print "Menu Based Matches"
	menu_based_matches = get_candidate_menu_items.get_menu_base_matches(menudict, tokens)
	menu_based_matches_sorted = sorted(menu_based_matches.items(), key=itemgetter(1),reverse=True)
	for i in range(0,30):
		print menu_based_matches_sorted[i]

	candidate_menu_items_by_prefix_sorted = sort_candidates(candidate_menu_items_by_prefix,menudict)
	#print "BY PREFIX"
	#counter = 0
	#max_items_to_print = 20
	#for item in candidate_menu_items_by_prefix_sorted:
	#	counter+= 1
	#	if counter < max_items_to_print:
	#		print(item['candidate_menu_item'],item['total_extractions'],item['extraction_score'])

	#print "BY SUFFIX"
	candidate_menu_items_by_suffix_sorted = sort_candidates(candidate_menu_items_by_suffix,menudict)
	#counter = 0
	#for item in candidate_menu_items_by_suffix_sorted:
	#	counter+= 1
        #        if counter < max_items_to_print:
        #		print(item['candidate_menu_item'],item['total_extractions'],item['extraction_score'])
	
	print "Aggregated Results"
	ag_results = aggregate_all_candidates(candidate_menu_items_by_prefix_sorted + candidate_menu_items_by_suffix_sorted)
	for i in range(0,30):
		print ag_results[i]
	#score = compare_with_actual_menu(results, biz)

def sort_candidates(cands,menudict):
	for item in cands:
		exists,freq = DictLookUp.look_up_in_menu_dict(item['candidate_menu_item'],menudict)
		if exists:
			item['extraction_score'] = item['extraction_score']**2
	#sort by extraction_score
	cands_sorted = sorted(cands, key=itemgetter('extraction_score'),reverse=True)
	return cands_sorted

def aggregate_all_candidates(cands):
	resultcand = dict()
	for item in cands:
		if item['candidate_menu_item'] in resultcand:
			resultcand[item['candidate_menu_item']] += item['extraction_score']
		else:
			resultcand[item['candidate_menu_item']] = item['extraction_score']
	cands_sorted = sorted(resultcand.items(), key=itemgetter(1),reverse=True)
	return cands_sorted

#finds businesses that have the most reviews and returns a list of ids and review count
def get_bizids_with_lots_reviews(allbiz,n):
	bizid_revcount = {}
	for bizid in allbiz:
		thebiz = allbiz[bizid]
		if 'review' in thebiz:
			bizid_revcount[bizid] = len(thebiz['review'])
	return helpers.get_top_n_from_dict(bizid_revcount,n)

if __name__ == "__main__":
	master_pipeline()
