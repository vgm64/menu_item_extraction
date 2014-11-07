import ujson as json
import operator

def aggregate_pattern_support(filename, outputdir):
    suffixes = dict()
    prefixes = dict()
    suffix_prefix_pairs = dict()
    with open(filename, 'r') as f:
        for line in f:
            pattern = json.loads(line)
            suffix = pattern['suffix']
            prefix = pattern['prefix']
            item = pattern['item']
            if suffix in suffixes:
                suffixes[suffix] = suffixes[suffix] + 1
            else:
                suffixes[suffix] = 1
            
            if prefix in prefixes:
                prefixes[prefix] = prefixes[prefix] + 1
            else:
                prefixes[prefix] = 1
            
            pair = prefix+"|"+suffix
            if pair in suffix_prefix_pairs:
                suffix_prefix_pairs[pair] = suffix_prefix_pairs[pair] + 1
            else:
                suffix_prefix_pairs[pair] = 1
        
            
        suffixes = sorted(suffixes.items(), key=operator.itemgetter(1),reverse=True)
        out = open(outputdir+"suffix_support", 'w')
        for suffix in suffixes:
            output = dict()
            output['phrase'] = suffix[0]
            output['support'] = suffix[1]
            json.dump(output, out)
            out.write("\n")
        out.close()
        
        prefixes = sorted(prefixes.items(), key=operator.itemgetter(1),reverse=True)
        out = open(outputdir+"prefix_support", 'w')
        for prefix in prefixes:
            output = dict()
            output['phrase'] = prefix[0]
            output['support'] = prefix[1]
            json.dump(output, out)
            out.write("\n")
        out.close()
        
        suffix_prefix_pairs = sorted(suffix_prefix_pairs.items(), key=operator.itemgetter(1),reverse=True)
        out = open(outputdir+"suffix_prefix_pair_support", 'w')
        for pair in suffix_prefix_pairs:
            output = dict()
            output['phrase'] = pair[0]
            output['support'] = pair[1]
            json.dump(output, out)
            out.write("\n")
        out.close()

aggregate_pattern_support("/scratch/mariachr/menu_item_extraction/data/raw_extracted_patterns","/scratch/mariachr/menu_item_extraction/data/")
