import pickle

def load_menu_dictionary(path,filename):
	prefix_file_str = path + '/' + filename
	menu_dict = pickle.load( open( prefix_file_str, "rb" ) )
	return menu_dict

#returns if item exists in menu and its associated frequency
def look_up_in_menu_dict(item,menu_dict):
	if item in menu_dict:
		return True,menu_dict[item]
	else:
		return False,0
