from nltk.corpus import stopwords
import DictLookUp
import master_pipeline
stopset = set(('a', 'about', 'above', 'after', 'again', 'all', 'am', 'an', 'and',
 'any', 'are', 't', 'as', 'at', 'be', 'because', 'been', 'before',
 'being', 'below', 'between', 'both', 'but', 'by', 'cannot', 'could',
 'd', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few',
 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he',
 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i',
 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'll', 'm', 'me',
 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off',
 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves',
 'out', 'over', 'own', 're', 'same', 'she', 'should', 'shouldn', 'so',
 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them',
 'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very',
 'was', 'wasn', 'we', 'were', 'weren', 'what', 'when', 'where', 'which',
 'while', 'who', 'whom', 'why', 'with', 'would', 'wouldn', 'you', 'your',
 'yours', 'yourself', 'yourselves'))

def get_max_phrase_length(phrases):
    max_length = 0
    min_length = 10000
    for phrase in phrases:
        phrase_length = len(phrase.split(" "))
        if phrase_length > max_length:
            max_length = phrase_length
        if phrase_length < min_length:
            min_length = phrase_length
    return max_length, min_length
    
def convert_phrase_list_to_dictionary(phrase_list):
    phrases = dict()
    for phrase_item in phrase_list:
        phrases[phrase_item['phrase']] = phrase_item['support']
    return phrases
    
def aggregate_phrase_occurances(occurances):
    phrases = dict()
    names_with_varrying_capitalization = set()
    extraction_score = 0
    for phrase in occurances:
        if len(phrase[0]) == 0:
            continue
	support = phrase[1]
	names_with_varrying_capitalization.add(phrase[2])
	extraction_score+= support
        if phrase[0] not in phrases:
        	phrases[phrase[0]] = [support, 1]
        else:
           	current_count = phrases[phrase[0]][1]
            	phrases[phrase[0]] = [support, current_count + 1]
    return phrases, extraction_score, names_with_varrying_capitalization

def convert_to_output_format(candidate_menu_items):
    output = []
    for candidate_menu_item in candidate_menu_items:
	# ignore extracted phrases whose tokens are more than 50% stopwords
    	candidate_menu_item_tokens = candidate_menu_item.lower().split(" ")
	candidate_menu_item_tokens_no_stopwords = [w for w in candidate_menu_item_tokens if not w in stopset]
	if float(len(candidate_menu_item_tokens_no_stopwords))/len(candidate_menu_item_tokens) > 0.5:
        	extraction_info, extraction_score,names_with_varrying_capitalization = aggregate_phrase_occurances(candidate_menu_items[candidate_menu_item])
        	output_item = dict()
        	output_item['candidate_menu_item'] = candidate_menu_item
        	total_extractions = len(candidate_menu_items[candidate_menu_item])
		output_item['total_extractions'] = total_extractions
		output_item['distinct_phrase_extractions'] = len(extraction_info)
		output_item['extraction_score'] = extraction_score
		output_item['varrious_capitalizations'] = names_with_varrying_capitalization
		extractions = []
        	for prefix in extraction_info:
        		extraction = dict()
        		extraction['phrase'] = prefix
        		extraction['phrase_support'] = extraction_info[prefix][0]
        		extraction['frequency'] = extraction_info[prefix][1]
        		extractions.append(extraction)
        	output_item['extractions'] = extractions
        	output.append(output_item)
    return output

def extract_candidate_menu_items_from_prefix(tokens, prefix_list, menu_item_length):
	prefixes = convert_phrase_list_to_dictionary(prefix_list)
	max_length, min_length = get_max_phrase_length(prefixes) 
	candidate_menu_items = dict()
	for i in range(0,len(tokens)):
        	for j in range(i + min_length, i + max_length + 1):
            		prefix_candidate = " ".join(tokens[i:j])
            		if prefix_candidate in prefixes:
                		menu_item_candidate = " ".join(tokens[j:min(j + menu_item_length, len(tokens))])
				menu_item_candidate_lower = menu_item_candidate.lower()
				if len(tokens) - j >= 1:
                    			occurance = [prefix_candidate,prefixes[prefix_candidate],menu_item_candidate]
                    			if menu_item_candidate_lower not in candidate_menu_items:
                        			candidate_menu_items[menu_item_candidate_lower] = []
                    			candidate_menu_items[menu_item_candidate_lower].append(occurance)          
	return convert_to_output_format(candidate_menu_items)

def extract_candidate_menu_items_from_suffix(tokens, suffix_list, menu_item_length):
    suffixes = convert_phrase_list_to_dictionary(suffix_list)
    max_length, min_length = get_max_phrase_length(suffixes) 
    candidate_menu_items = dict()
    for i in range(0,len(tokens)):
        for j in range(i + min_length, i + max_length + 1):
            suffix_candidate = " ".join(tokens[i:j])
	    if suffix_candidate in suffixes:
                menu_item_candidate = " ".join(tokens[max(i - menu_item_length, 0):i])
		menu_item_candidate_lower = menu_item_candidate.lower()
		if i > 0:
                    occurance = [suffix_candidate,suffixes[suffix_candidate],menu_item_candidate]
                    if menu_item_candidate_lower not in candidate_menu_items:
                        candidate_menu_items[menu_item_candidate_lower] = []
                    candidate_menu_items[menu_item_candidate_lower].append(occurance)
    return convert_to_output_format(candidate_menu_items)

def get_menu_base_matches(menu_dict, tokens):
	found_in_menus = dict()
	max_length, min_length = get_max_phrase_length(menu_dict)
	for i in range(0,len(tokens)-max_length):
		for j in range(i + min_length, i + max_length + 1):
			menu_item_candidate = " ".join(tokens[i:j])
			if menu_item_candidate in menu_dict and len(menu_item_candidate.split(" ")) > 1:
				if menu_item_candidate not in found_in_menus:
					found_in_menus[menu_item_candidate] = 0
				found_in_menus[menu_item_candidate]+= 1
	return found_in_menus

def extract_candidate_menu_items(tokens, prefix_list, suffix_list):
	output = []
	menu_dict = DictLookUp.load_menu_dictionary("/scratch/mariachr/menu_item_extraction/data/","menudict.p")
	bigrams_suffix = extract_candidate_menu_items_from_suffix(tokens, suffix_list, 2)
	bigrams_prefix = extract_candidate_menu_items_from_prefix(tokens, prefix_list, 2)
	bigrams_suffix_dict = dict()
	bigrams_prefix_dict = dict()
	for item in bigrams_suffix:
		bigrams_suffix_dict[item['candidate_menu_item']] = item
	for item in bigrams_prefix:
                bigrams_prefix_dict[item['candidate_menu_item']] = item

	to_remove_from_bigrams = set()
	trigrams_suffix = extract_candidate_menu_items_from_suffix(tokens, suffix_list, 3)
        for item in trigrams_suffix:
                candidate_menu_item = item['candidate_menu_item']
		first_bigram = " ".join(candidate_menu_item.split(" ")[0:2])
		second_bigram = " ".join(candidate_menu_item.split(" ")[1:3])
		if first_bigram in bigrams_prefix_dict and second_bigram in bigrams_suffix_dict:
			#if float(item['extraction_score'])/bigrams_suffix[second_bigram]['extraction_score'] > 0.9
			#	del bigrams_suffix[second_bigram]
			to_remove_from_bigrams.add(first_bigram)
			to_remove_from_bigrams.add(second_bigram)
			output.append(item)

	trigrams_prefix = extract_candidate_menu_items_from_prefix(tokens, suffix_list, 3)
	for item in trigrams_prefix:
                candidate_menu_item = item['candidate_menu_item']
                first_bigram = " ".join(candidate_menu_item.split(" ")[0:2])
                second_bigram = " ".join(candidate_menu_item.split(" ")[1:3])
                if first_bigram in bigrams_prefix_dict and second_bigram in bigrams_suffix_dict:
                        output.append(item)
			to_remove_from_bigrams.add(first_bigram)
                        to_remove_from_bigrams.add(second_bigram)
	
	print "Got %s  triplets" % str(len(output))
	for item in bigrams_suffix_dict:
		if item not in to_remove_from_bigrams:
			output.append(bigrams_suffix_dict[item])

	for item in bigrams_prefix_dict:
                if item not in to_remove_from_bigrams:
                        output.append(bigrams_prefix_dict[item])

	output = master_pipeline.sort_candidates(output,menu_dict)
	#sort_candidates
	count = 0
	for item in output:
		candidate_menu_item_tokens = item['candidate_menu_item'].split(" ")
		if len(candidate_menu_item_tokens) > 2:
			count+= 1
			if count > 10:
				return
			print "%s  with score %s" % (item['candidate_menu_item'],str(item['extraction_score']))

	
