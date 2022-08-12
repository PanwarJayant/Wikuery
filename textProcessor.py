from nltk.corpus import stopwords as sw
from nltk.stem import PorterStemmer as ps
import re


def tokenization(formatted_text):
    return formatted_text.split()


def cleaning(text, isBody=False):
    # Lower the case
    text = text.lower()

    # Removing unwanted characters (ONLY for body text)
    if isBody:
        text = text.replace('\n', ' ')
        text = text.replace('File:', ' ')
        text = re.sub('(http://[^ ]+)', ' ', text)
        text = re.sub('(https://[^ ]+)', ' ', text)
        text = re.sub('\{.*?\}|\[.*?\]|\=\=.*?\=\=', ' ', text)

    # Removing non-ASCII
    formatted_text = ''
    for char in text:
        if(ord(char) < 128):
            formatted_text += char
        else:
            formatted_text += ' '

    # Removing HTML Tags
    formatted_text = re.sub(html_tags, ' ', formatted_text)

    # Removing Special Chars
    for char in formatted_text:
        if not char.isalnum():
            formatted_text = formatted_text.replace(char, ' ')

    # Split into tokens
    formatted_text = tokenization(formatted_text)

    # Remove stopWords
    processed_text = []
    for word in formatted_text:
        if word in stopwords:
            continue
        else:
            processed_text.append(word)

    return processed_text


def stemming(processed_text):
    stemmed_text = []
    for word in processed_text:
        stemmed_text.append(stemmer.stem(word))

    return stemmed_text


def processText(text, isBody=False):
    text = cleaning(text, isBody)
    text = stemming(text)
    return text


html_tags = re.compile('&amp;|&apos;|&gt;|&lt;|&nbsp;|&quot;')
stemmer = ps()
stopwords = set(sw.words('english'))
