import time
import xml.sax
from xml.sax.handler import feature_namespaces
import wikiProcessor
from handler import *
from collections import defaultdict


class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tag = ''
        self.title = ''
        self.text = ''

    def startElement(self, name, attrs):
        self.tag = name

    def endElement(self, name):
        global num_pages
        global id_title_map
        if name == "page":
            print(num_pages)
            id_title_map[num_pages] = self.title.lower()
            title = wikiProcessor.processTitle(self.title)
            infobox, body_text, references, links, categories = wikiProcessor.processBody(
                self.text)
            createIndex(title, body_text, categories,
                        infobox, links, references)
            self.tag = ""
            self.title = ""
            self.text = ""

    def characters(self, content):
        if self.tag == "title":
            self.title += content
        if self.tag == "text":
            self.text += content


def updateComponents(words_set, component, dict):
    words_set.update(component)
    for part in component:
        dict[part] += 1
    return words_set, dict


def updatePosting(posting, dict, word, char):
    if dict[word]:
        posting += char
        posting += str(dict[word])
    posting += ';'
    return posting


def createIndex(title, body, category, infobox, link, reference):
    global num_files
    global num_pages
    global index_map
    global id_title_map
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

            index_map[word] += posting

    num_pages += 1

    if not(num_pages % 35000):
        num_files = writeIntIndex(num_files, index_map)
        writeIDmap(id_title_map)
        index_map = defaultdict(str)
        id_title_map = {}


start = time.time()

num_files = 0
num_pages = 0
index_map = defaultdict(str)
id_title_map = {}

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler, feature_namespaces, False)
xml_handler = XMLHandler()
parser.setContentHandler(xml_handler)
output = parser.parse(getInputFile())

num_files = writeIntIndex(num_files, index_map)
writeIDmap(id_title_map)

end = time.time()
print("Total indexing time: ", end-start)
