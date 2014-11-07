import ujson as json

def get_phrases(prefix_filename, suffix_filename, path):

    prefix_file = open(path + '/' + prefix_filename)
    suffix_file = open(path + '/' + suffix_filename)
    
    prefix_data = []
    for line in prefix_file:
        prefix_data.append(json.loads(line))

    suffix_data = []
    for line in suffix_file:
        suffix_data.append(json.loads(line))

    return prefix_data, suffix_data

def get_biz_data(biz_data_filename, path):
    
    biz_data_file = open(path + '/' + biz_data_filename)
    biz_data = json.load(biz_data_file)
    return biz_data

def load_phrases_and_biz_data(prefix_filename, suffix_filename, biz_data_filename, path):

    prefix_data, suffix_data = get_phrases(prefix_filename, suffix_filename, path)
    biz_data = get_biz_data(biz_data_filename, path)

    return prefix_data, suffix_data, biz_data

