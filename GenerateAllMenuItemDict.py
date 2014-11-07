import ujson

allitems = []

def get_menu_line():
    dir = '/scratch/mariachr/menu_item_extraction/data/menutest2'
    with open(dir, 'r') as f:
        for line in f:
            menu = line.split("\t")[1]
            menu_items = []
            try:
                menu_json = ujson.loads(menu.replace("\\\\", "\\"))
                for menu_item in menu_json['sub_menus']:
                    for section in menu_item['sections']:
                        items = section['items']
                        for item in items:
                            if 'name' in item:
                                item_name = item['name'].lower()
                                menu_items.append(item_name)
                yield menu_items
            except ValueError, e:
                yield ""
