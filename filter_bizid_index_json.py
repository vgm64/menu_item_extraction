import ujson as json
import sys

INPUT_FILE = '../data/biz_id_index_menu_and_review.json'
OUTPUT_FILE = '../data/biz_id_index_menu_and_review_filtered.json'

def filter_by_review_length(data, length):
    """ Remove reviews that are of less than a given number of words."""

    for biz_id in data:
        reviews = data[biz_id]['review']
        #reviews[:] = filter(lambda x: x['comment'].split() > length, reviews)
        reviews[:] = filter(lambda x: len(x['comment'].split()) > length, data[biz_id]['review'])

        #data[biz_id]['review'] = filter(lambda x: x['comment'].split() > length, data[biz_id]['review'])

def get_data(input_filename):
    input_file = open(input_filename)
    data = json.load(input_file)
    return data

def write_data(data, output_filename):
    output_file = open(output_filename, 'w')
    json.dump(data, output_file)

if __name__ == '__main__':
    print "Reading data"
    data = get_data(INPUT_FILE)
    print "I have %d keys in data" % sum(len(data[key]['review']) for key in data)
    print "Filtering..."
    filter_by_review_length(data, 20)
    print "Now I have %d keys in data" % sum(len(data[key]['review']) for key in data)
    print "Writing file"
    write_data(data, OUTPUT_FILE) 
    print "Done"


