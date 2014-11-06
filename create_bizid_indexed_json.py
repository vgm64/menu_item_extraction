import ujson as json
import sys

REVIEW_BIZ_FILE = '../data/sf_reviews_jan12013_to_nov2014'
MENU_FILE = '../data/menutest2'
ALL_DATA_OUTPUT_FILE = '../data/biz_id_index_menu_and_or_review.json'
BOTH_MENU_AND_REVIEWS_OUTPUT_FILE = '../data/biz_id_index_menu_and_review.json'

NUM_LINES_TO_UPDATE = 1000


def read_files(review_file, menu_file):
    review_biz_file = open(review_file)
    review_header = review_biz_file.readline().split("\t")

    result_dict = {}
        
    num_lines = 0
    for line in review_biz_file:
        num_lines += 1
        if num_lines % NUM_LINES_TO_UPDATE == 0:
            print "Working on review data line %d \r" % (num_lines),
            sys.stdout.flush()
        fields = line.split("\t")
        review_dict = dict(zip(review_header, fields))
        biz_id = review_dict['id']


        if 'review' not in result_dict[biz_id]:
            result_dict[biz_id]['review'] = []

        result_dict[biz_id]['review'].append(review_dict)

    menu_file = open(menu_file)
    menu_header = menu_file.readline().split("\t")

    print "Working on review data line %d \r" % (num_lines)
    num_lines = 0
    for line in menu_file:
        num_lines += 1
        if num_lines % NUM_LINES_TO_UPDATE == 0:
            print "Working on menu line %d \r" % (num_lines),
            sys.stdout.flush()
        fields = line.split("\t")
        menu_dict = dict(zip(menu_header, fields))
        biz_id = menu_dict['business_id']
        result_dict.setdefault(biz_id, {})

        if 'menu' not in result_dict[biz_id]:
            result_dict[biz_id]['menu'] = []
        if 'menu' and 'review' in result_dict[biz_id]:
            result_dict[biz_id]['menu_and_reviews'] = True

        result_dict[biz_id]['menu'].append(menu_dict)

    print "Working on menu line %d \r" % (num_lines)



    return result_dict


def write_all(all_data):
    print "Writing unfiltered data to disk."
    all_output_file = open(ALL_DATA_OUTPUT_FILE, "w")
    json.dump(all_data, all_output_file)
    print "Data written to", ALL_DATA_OUTPUT_FILE

def write_menu_plus_reviews_subset(data):
    print "Generating subset of data with menus and reviews"

    data_with_menu_and_reviews = {}
    for key in data:
        if data[key].has_key('menu_and_reviews'):
            data_with_menu_and_reviews[key] = data[key]
    print "Writing the subset to disk"
    subset_output_file = open(BOTH_MENU_AND_REVIEWS_OUTPUT_FILE, 'w')
    json.dump(data_with_menu_and_reviews, subset_output_file)
    print "Done writing file to disk."


if __name__ == '__main__':
    all_data = read_files(REVIEW_BIZ_FILE, MENU_FILE)

    write_all(all_data)
    write_menu_plus_reviews_subset(all_data)
    
    print "Done"
