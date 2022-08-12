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
