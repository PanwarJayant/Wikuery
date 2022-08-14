import sys
import os
from tqdm import tqdm
import re
from collections import defaultdict


def getInputFile():
    if(len(sys.argv) <= 1):
        print("ERROR: Please enter path to XML dump!")
        exit()
    return sys.argv[1]


def initializeDicts(type):
    title_dict = defaultdict(type)
    body_dict = defaultdict(type)
    category_dict = defaultdict(type)
    infobox_dict = defaultdict(type)
    link_dict = defaultdict(type)
    reference_dict = defaultdict(type)
    return title_dict, body_dict, category_dict, infobox_dict, link_dict, reference_dict


def writeIDmap(id_title_map):
    temp_id_title = []
    # temp_id_title_map = sorted(
    #     id_title_map.items(), key=lambda item: int(item[0]))
    temp_id_title_map = sorted(id_title_map.items())

    for id, title in tqdm(temp_id_title_map):
        t = str(id)+'-'
        t += title.strip()
        temp_id_title.append(t)

    os.mkdir("./indexing")
    file = open("./indexing/id_title_map.txt", 'a')
    file.write('\n'.join(temp_id_title))
    file.write('\n')
    file.close()


def writeIntIndex(num_files, index_map):
    temp_index_map = sorted(index_map.items())
    # temp_index_map = sorted(index_map.items(), key=lambda item: item[0])
    temp_index = []
    for word, posting in tqdm(temp_index_map):
        toAppend = word+'-'+posting
        temp_index.append(toAppend)

    file = open("./indexing/index_{num_files}.txt", "w")
    file.write('\n'.join(temp_index))
    file.close()
    num_files += 1
    return num_files


def searchAndGroup(char, dict, fields, token, id):
    if char in fields:
        dict[token][id] = re.search(r'.*'+char+'([0-9]*).*', fields).group(1)
    return dict


def getDiffPosting(token, posting, final_components):
    postings = sorted(posting.items())
    # postings = sorted(posting.items(), key=lambda item: int(item[0]))

    final_posting = token+'-'

    for id, freq in postings:
        final_posting += str(id)+":"+freq+';'

    final_components.append(final_posting.rstrip(';'))

    return final_components


def writeDiffPosting(type, final_components, final_num_files):
    path = "./indexing/" + type + \
        "_data_" + str(final_num_files) + ".txt"
    file = open(path, "w")
    file.write('\n'.join(final_components))
    file.close()


def updateInfo(token, dict, final_components, unique_token_info):
    if token in dict.keys():
        posting = dict[token]
        final_components = getDiffPosting(token, posting, final_components)
        t_len = len(final_components)
        unique_token_info[token] += str(t_len)

    unique_token_info[token] += '-'

    return final_components, unique_token_info


def writeFiles(merge_data, final_num_files):
    title_dict, body_dict, category_dict, infobox_dict, link_dict, reference_dict = initializeDicts(
        dict)

    unique_token_info = {}

    sorted_data = sorted(merge_data)
    # sorted_data = sorted(merge_data.items(), key=lambda item:item[0])

    enumerated_data = enumerate(sorted_data)

    for i, (token, postings) in tqdm(enumerated_data):
        for posting in postings.split(';')[:-1]:
            id = posting.split(':')[0]
            fields = posting.split(':')[1]

            title_dict = searchAndGroup('t', title_dict, fields, token, id)
            body_dict = searchAndGroup('b', body_dict, fields, token, id)
            category_dict = searchAndGroup(
                'c', category_dict, fields, token, id)
            infobox_dict = searchAndGroup('i', infobox_dict, fields, token, id)
            link_dict = searchAndGroup('l', link_dict, fields, token, id)
            reference_dict = searchAndGroup(
                'r', reference_dict, fields, token, id)

        token_info = '-'.join([token, str(final_num_files),
                               str(len(postings.split(';')[:-1]))])
        unique_token_info[token] = token_info+'-'

    final_titles, final_body_text, final_categories, final_infoboxes, final_links, final_references = ([
    ] for i in range(6))

    for i, (token, j) in tqdm(enumerated_data):
        final_titles, unique_token_info = updateInfo(
            token, title_dict, final_titles, unique_token_info)
        final_body_text, unique_token_info = updateInfo(
            token, body_dict, final_body_text, unique_token_info)
        final_categories, unique_token_info = updateInfo(
            token, category_dict, final_categories, unique_token_info)
        final_infoboxes, unique_token_info = updateInfo(
            token, infobox_dict, final_infoboxes, unique_token_info)
        final_links, unique_token_info = updateInfo(
            token, link_dict, final_links, unique_token_info)
        final_references, unique_token_info = updateInfo(
            token, reference_dict, final_references, unique_token_info)

    file = open("./indexing/tokens_info.txt", "a")
    file.write('\n'.join(unique_token_info.values()))
    file.write('\n')
    file.close()

    writeDiffPosting('title', final_titles, final_num_files)
    writeDiffPosting('body', final_body_text, final_num_files)
    writeDiffPosting('category', final_categories, final_num_files)
    writeDiffPosting('infobox', final_infoboxes, final_num_files)
    writeDiffPosting('link', final_links, final_num_files)
    writeDiffPosting('reference', final_references,  final_num_files)

    final_num_files += 1
    return final_num_files
