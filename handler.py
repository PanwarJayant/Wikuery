from heapq import merge
from importlib.metadata import files
from lib2to3.pgen2 import token
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
    temp_id_title_map = sorted(
        id_title_map.items(), key=lambda item: int(item[0]))
    # temp_id_title_map = sorted(id_title_map.items())

    temp_id_title = []
    for id, title in tqdm(temp_id_title_map):
        t = str(id)+'-'
        t += title.strip()
        temp_id_title.append(t)

    file = open("./indexing/id_title_map.txt", 'a')
    file.write('\n'.join(temp_id_title))
    file.write('\n')
    file.close()


def writeIntIndex(num_files, index_map):
    temp_index = []
    # temp_index_map = sorted(index_map.items())
    temp_index_map = sorted(index_map.items(), key=lambda item: item[0])
    for word, posting in tqdm(temp_index_map):
        toAppend = word+'-'+posting
        temp_index.append(toAppend)

    file = open(f"./indexing/index_{num_files}.txt", "w")
    file.write('\n'.join(temp_index))
    file.close()
    num_files += 1
    return num_files


def searchAndGroup(char, dict, fields, token, id):
    if char in fields:
        dict[token][id] = re.search(r'.*'+char+'([0-9]*).*', fields).group(1)
    return dict


def getDiffPosting(token, posting, final_components, isDiff=True):
    # postings = sorted(posting.items())
    postings = sorted(posting.items(), key=lambda item: int(item[0]))

    if isDiff:
        final_posting = token+'-'

        for id, freq in postings:
            final_posting += str(id)+":"+freq+';'

    final_components.append(final_posting.rstrip(';'))

    return final_components


def writeDiffPosting(type, final_components, final_num_files):
    # path = "./indexing/" + type + \
    #     "_data_" + str(final_num_files) + ".txt"
    file = open(f"./indexing/{type}_data_{str(final_num_files)}.txt", "w")
    file.write('\n'.join(final_components))
    file.close()


def updateInfo(token, dict, final_components, unique_token_info):
    if token in dict.keys():
        posting = dict[token]
        final_components = getDiffPosting(token, posting, final_components)
        unique_token_info[token] += str(len(final_components))

    unique_token_info[token] += '-'

    return final_components, unique_token_info


def writeFiles(merge_data, final_num_files):
    title_dict, body_dict, category_dict, infobox_dict, link_dict, reference_dict = initializeDicts(
        dict)

    unique_token_info = {}

    # sorted_data = sorted(merge_data)
    sorted_data = sorted(merge_data.items(), key=lambda item: item[0])

    # enumerated_data = enumerate(sorted_data)

    for i, (token, postings) in tqdm(enumerate(sorted_data)):
        splits = postings.split(';')[:-1]
        for posting in splits:
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
                               str(len(splits))])
        unique_token_info[token] = token_info+'-'

    final_titles, final_body_text, final_categories, final_infoboxes, final_links, final_references = ([
    ] for i in range(6))

    for i, (token, j) in tqdm(enumerate(sorted_data)):
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


def mergeFiles(num_itermed_files):
    files_data, line, postings = ({} for i in range(3))
    is_file_empty = {i: 1 for i in range(num_itermed_files)}
    tokens = []

    for i in range(num_itermed_files):
        files_data[i] = open(f'./indexing/index_{i}.txt', 'r')
        stripped = files_data[i].readline().strip('\n')
        line[i] = stripped
        postings[i] = stripped.split('-')
        is_file_empty[i] = 0
        new_token = postings[i][0]
        if postings[i][0] not in tokens:
            tokens.append(new_token)

    tokens.sort(reverse=True)
    num_processed_postings = 0
    merge_data = defaultdict(str)
    final_num_files = 0

    while sum(is_file_empty.values()) != num_itermed_files:
        token = tokens.pop()
        num_processed_postings += 1
        if not (num_processed_postings % 30000):
            final_num_files = writeFiles(merge_data, final_num_files)
            merge_data = defaultdict(str)

        i = 0
        while i < num_itermed_files:
            if not is_file_empty[i]:
                if token == postings[i][0]:
                    line[i] = files_data[i].readline()
                    line[i] = line[i].strip('\n')
                    merge_data[token] += postings[i][1]

                    if len(line[i]) > 0:
                        postings[i] = line[i].split('-')
                        new_token = postings[i][0]

                        if postings[i][0] not in tokens:
                            tokens.append(new_token)
                            tokens.sort(reverse=True)

                    elif len(line[i]) == 0:
                        is_file_empty[i] = 1
                        files_data[i].close()
                        if os.path.exists(f"./indexing/index_{str(i)}.txt"):
                            print(f"Removing file {str(i)}")
                            os.remove(f"./indexing/index_{str(i)}.txt")
            i += 1

    final_num_files = writeFiles(merge_data, final_num_files)
    return final_num_files


def writeProcessInfo(var, path):
    full_path = "./indexing/"+path+".txt"
    file = open(full_path, "w")
    file.write(str(var))
    file.close()
