import ujson as json
from nltk.tokenize import RegexpTokenizer

def exctract_pattern_from_review(menu_items, reviews, max_length):
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    prefix_span = 3
    suffix_span = 3
    output = []
    
    for review in reviews:
        review_text = review['comment']
        review_text = review_text.replace("\\n"," ")
        review_text = review_text.replace("\n"," ").lower()
        all_words = tokenizer.tokenize(review_text)
        for i in range(0,len(all_words)):
            for j in range(i + 1, i + max_length+1):
                item_candidate = " ".join(all_words[i:j])
                if item_candidate in menu_items:
                    pattern = dict()
                    pattern['prefix'] =  " ".join(all_words[max(i - prefix_span,0):i])
                    pattern['suffix'] =  " ".join(all_words[j:min(j + suffix_span,len(all_words))])
                    pattern['item'] = item_candidate
                    output.append(pattern)
    return output

def process_business(all_businesses, output_filename):
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    outfile = open(output_filename, 'w')
    line_counter = 0
    # Each line is a business
    biz_counter = 0
    biz_skipped = 0
    for business_id in all_businesses:
        business = all_businesses[business_id]
        if 'review' in business:
            reviews = business['review']
            if 'menu' in business:
                menu = business['menu'][0]
                basic_menu = menu['menu']
                try:
                    basic_menu = json.loads(basic_menu.replace("\\\\", "\\"))
                    biz_counter+= 1
                except:
                    print(business_id)
                    biz_skipped+= 1
                    continue
                all_menu_items = set()
                menu_item_max_length = 1
                for menu_item in basic_menu['sub_menus']:
                    for section in menu_item['sections']:
                        items = section['items']
                        for item in items:
                            if 'name' in item:
                                item_name = item['name'].lower()
                                item_name = item_name.replace("\\n"," ")
                                item_name = item_name.replace("\n"," ")
                                tokens = tokenizer.tokenize(item_name)
                                item_name = " ".join(tokens)
                                all_menu_items.add(item_name)
                                length = len(tokens)
                                if length > menu_item_max_length:
                                    menu_item_max_length = length
            #print(menu_items)
            patterns = exctract_pattern_from_review(all_menu_items, reviews, menu_item_max_length)
            for pattern in patterns:
                json.dump(pattern, outfile)
                outfile.write("\n")
                line_counter = line_counter + 1
                if line_counter%1000 == 0:
                    print "Done with %s lines. %s businesses OK and %s businesses skipped!" % (str(line_counter),str(biz_counter),str(biz_skipped))
    outfile.close()

all_businesses = json.load(open("/scratch/mariachr/menu_item_extraction/data/biz_id_index_menu_and_review.json"))
process_business(all_businesses,"/scratch/mariachr/menu_item_extraction/data/raw_extracted_patterns")
