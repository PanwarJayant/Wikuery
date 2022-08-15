import pstats
import time
import xml.sax
from xml.sax.handler import feature_namespaces
import wikiProcessor
from handler import *
from collections import defaultdict
import cProfile


class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tag = ''
        self.title = ''
        self.text = ''

    def startElement(self, name, attrs):
        self.tag = name

    def characters(self, content):
        if self.tag == "title":
            self.title += content
        elif self.tag == "text":
            self.text += content

    def endElement(self, name):
        global num_pages
        global id_title_map
        global text_tokens
        if name == "page":
            print("Page no: ", num_pages)
            id_title_map[num_pages] = self.title.lower()
            title = wikiProcessor.processTitle(self.title)
            infobox, body_text, references, links, categories, text_tokens = wikiProcessor.processBody(
                self.text, text_tokens)
            createIndex(title, body_text, categories,
                        infobox, links, references)
            self.tag = ""
            self.title = ""
            self.text = ""


def updateComponents(words_set, component, dict):
    words_set.update(component)
    for part in component:
        dict[part] += 1
    return words_set, dict


def updatePosting(posting, dict, word, char):
    if dict[word]:
        posting += char
        posting += str(dict[word])
    return posting


def updateTokenCounts(list=[]):
    token_count = 0
    global output_path

    if not list:
        try:
            file = open(f"{output_path}/tokens_info_others.txt", "r")
            token_count += 1
            file.close()
        except FileNotFoundError:
            pass

        file = open(f"{output_path}/tokens_info_others_count.txt", "w")
        file.write(str(token_count))
        file.close()

    else:
        for part in tqdm(list):
            token_count = 0
            file = open(f"{output_path}/tokens_info_{part}.txt", "r")
            for line in file:
                token_count += 1
            file.close()
            file = open(f"{output_path}/tokens_info_{part}_count.txt", "w")
            file.write(str(token_count))
            file.close()


def createIndex(title, body, category, infobox, link, reference):
    global num_files
    global num_pages
    global index_map
    global id_title_map
    global output_path
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

    for word in words_set:
        temp = re.sub(r'^((.)(?!\2\2\2))+$', r'\1', word)

        if not (len(temp) == len(word)):
            posting = str(num_pages)+':'
            posting = updatePosting(posting, title_dict, word, 't')
            posting = updatePosting(posting, body_dict, word, 'b')
            posting = updatePosting(posting, category_dict, word, 'c')
            posting = updatePosting(posting, infobox_dict, word, 'i')
            posting = updatePosting(posting, link_dict, word, 'l')
            posting = updatePosting(posting, reference_dict, word, 'r')
            posting += ';'

            index_map[word] += posting

    num_pages += 1

    if not(num_pages % 35000):
        num_files = writeIntIndex(num_files, index_map, output_path)
        writeIDmap(id_title_map)
        index_map = defaultdict(str)
        id_title_map = {}


start = time.time()

num_files = 0
num_pages = 0
index_map = defaultdict(str)
id_title_map = {}
text_tokens = set()

output_path = getOutputPath()
stat_file = getStatFile()

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, False)
xml_handler = XMLHandler()
parser.setContentHandler(xml_handler)

# COMMENTED CODE USED FOR PROFILING AND CHECKING TIME
# with cProfile.Profile() as pr:
output = parser.parse(getInputFile())
# stats = pstats.Stats(pr)
# stats.sort_stats(pstats.SortKey.TIME)
# stats.dump_stats(filename="stats.prof")

num_files = writeIntIndex(num_files, index_map, output_path)
writeIDmap(id_title_map)

final_num_files = mergeFiles(num_files)

writeProcessInfo(num_pages, "num_pages")
num_tokens_final = 0
file = open(f"{output_path}/tokens_info.txt", "r")
for line in file:
    num_tokens_final += 1
file.close()
writeProcessInfo(num_tokens_final, "num_tokens")

char_list = []
num_list = []
for i in range(97, 123):
    char_list.append(chr(i))
for i in range(0, 10):
    num_list.append(str(i))

file = open(f"{output_path}/tokens_info.txt", "r")
for line in tqdm(file):
    if (line[0] in char_list) or (line[0] in num_list):
        subfile = open(f"{output_path}/tokens_info_{line[0]}.txt", "a")
        subfile.write(line.strip())
        subfile.write('\n')
        subfile.close()

    else:
        subfile = open(f"{output_path}/tokens_info_others.txt", "a")
        subfile.write(line.strip())
        subfile.write('\n')
        subfile.close()
file.close()

updateTokenCounts(char_list)
updateTokenCounts(num_list)
updateTokenCounts()

os.remove(f"{output_path}/tokens_info.txt")
print("Total indexing tokens", num_tokens_final)
print("Total text tokens: ", len(text_tokens))
print("Total files: ", final_num_files)

file = open(f"{stat_file}", "w")
file.write(str(len(text_tokens)))
file.write('\n')
file.write(str(num_tokens_final))
file.close()

end = time.time()
print("Total indexing time: ", end-start)
