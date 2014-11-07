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
    for phrase in occurances:
        if len(phrase) == 0:
            continue
        support = phrase[1]
        if phrase[0] not in phrases:
            phrases[phrase[0]] = [support, 1]
        else:
            current_count = phrases[phrase[0]][1]
            phrases[phrase[0]] = [support, current_count + 1]
    return phrases

def convert_to_output_format(candidate_menu_items):
    output = []
    for candidate_menu_item in candidate_menu_items:
        extraction_info = aggregate_phrase_occurances(candidate_menu_items[candidate_menu_item])
        output_item = dict()
        output_item['candidate_menu_item'] = candidate_menu_item
        total_extractions = len(candidate_menu_items[candidate_menu_item])
	output_item['total_extractions'] = total_extractions
	output_item['distinct_phrase_extractions'] = len(extraction_info)
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
                if len(tokens) - j >= 1:
                    occurance = [prefix_candidate,prefixes[prefix_candidate]]
                    if menu_item_candidate not in candidate_menu_items:
                        candidate_menu_items[menu_item_candidate] = []
                    candidate_menu_items[menu_item_candidate].append(occurance)
                        
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
		if i > 0:
                    occurance = [suffix_candidate,suffixes[suffix_candidate]]
                    if menu_item_candidate not in candidate_menu_items:
                        candidate_menu_items[menu_item_candidate] = []
                    candidate_menu_items[menu_item_candidate].append(occurance)
    return convert_to_output_format(candidate_menu_items)

