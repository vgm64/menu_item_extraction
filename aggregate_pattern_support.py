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
            out.write(suffix[0]+"\t"+str(suffix[1])+"\n")
        out.close()
        
        prefixes = sorted(prefixes.items(), key=operator.itemgetter(1),reverse=True)
        out = open(outputdir+"prefix_support", 'w')
        for prefix in prefixes:
            out.write(prefix[0]+"\t"+str(prefix[1])+"\n")
        out.close()
        
        suffix_prefix_pairs = sorted(suffix_prefix_pairs.items(), key=operator.itemgetter(1),reverse=True)
        out = open(outputdir+"suffix_prefix_pair_support", 'w')
        for pair in suffix_prefix_pairs:
            out.write(pair[0]+"\t"+str(pair[1])+"\n")
        out.close()

aggregate_pattern_support("/scratch/mariachr/menu_item_extraction/data/raw_extracted_patterns","/scratch/mariachr/menu_item_extraction/data/")
