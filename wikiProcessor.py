from textProcessor import processText


def processTitle(title):
    processed_title = processText(title)
    return processed_title


def processInfobox(text):
    processed_infobox = []
    text = text.split('\n')
    start = "{{Infobox"
    end = "}}"
    start_idx = 0
    for str in text:
        if(start in str):
            break
        start_idx += 1
    text_data = []
    text_data.append(' ')
    start_idx += 1
    end_idx = len(text)
    for ch in range(start_idx, end_idx):
        if(text[ch] == end):
            break
        text_data.append(text[ch])

    infobox_data = ' '.join(text_data)
    processed_infobox = processText(infobox_data)
    return processed_infobox


def processBodyText(text):
    processed_body_text = []
    processed_body_text = processText(text, True)
    return processed_body_text


def processCategories(text):
    processed_categories = []
    try:
        text = text.split('\n')
        start = "[[Category:"
        end = "]]"
        start_idx = 0
        end_idx = len(text)
        for str in text:
            if(str.startswith(start)):
                break
            start_idx += 1
        text_data = []
        first_category = text[start_idx].replace(start, ' ')
        first_category = first_category.replace(end, ' ')
        text_data.append(first_category)
        start_idx += 1
        for id in range(start_idx, end_idx):
            if(text[id].endswith(end)):
                other_category = text[id].replace(start, ' ')
                other_category = other_category.replace(end, ' ')
                text_data.append(other_category)
            else:
                break
        category_data = ' '.join(text_data)
        processed_categories = processText(category_data)
    except IndexError:
        pass
    return processed_categories


def processReferencesOrLinks(text, isReference=False, isLink=False):
    processed_components = []
    components = ''
    splitter = ""
    if isReference:
        splitter = "==References"
    if isLink:
        splitter = "==External links=="
    text = text.split(splitter)
    if len(text) <= 1:
        return processed_components
    text_split = text[1].split("\n")[1:]
    for str in text_split:
        if str == '':
            break
        if str[0] == '*':
            str_split = str.split(' ')
            component = []
            for wrd in str_split:
                if "http" not in wrd:
                    component.append(wrd)
            component = ' '.join(component)
            components += ' '
            components += component
    processed_components = processText(components)
    return processed_components


def processBody(text):
    infobox = processInfobox(text)
    body_text = processBodyText(text)
    references = processReferencesOrLinks(text, isReference=True)
    links = processReferencesOrLinks(text, isLink=True)
    categories = processCategories(text)
    return infobox, body_text, references, links, categories
