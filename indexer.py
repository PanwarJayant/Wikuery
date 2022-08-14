import xml.sax
# import parser
from handler import *
from collections import defaultdict


def updateComponents(words_set, component, dict):
    words_set.update(component)
    for part in component:
        dict[part] += 1
    return words_set, dict


def createIndex(title, body, category, infobox, link, reference, num_pages, index_map, id_title_map):
    words_set = set()
    title_dict, body_dict, category_dict, infobox_dict, link_dict, reference_dict = initializeDicts(
        int)

    words_set, title_dict = updateComponents(words_set, title, title_dict)
    words_set, body_dict = updateComponents(words_set, body, body_dict)
    words_set, category_dict = updateComponents(
        words_set, category, category_dict)
    words_set, infobox_dict = updateComponents(
        words_set, infobox, infobox_dict)
    words_set, link_dict = updateComponents(words_set, link, link_dict)
    words_set, reference_dict = updateComponents(
        words_set, reference, reference_dict)
