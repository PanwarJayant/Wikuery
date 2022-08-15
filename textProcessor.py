from os import remove
from nltk.corpus import stopwords as sw
import Stemmer
import re


def countTextTokens(text, text_tokens):
    text = text.lower()
    tokens = text.split()
    for token in tokens:
        if token in text_tokens:
            text_tokens[token] += 1
        else:
            text_tokens[token] = 1
    return text_tokens


def tokenization(formatted_text):
    return formatted_text.split()


def cleanBodyText(text):
    text = text.replace('\n', ' ')
    text = text.replace('File:', ' ')
    text = re.sub('(http://[^ ]+)', ' ', text)
    text = re.sub('(https://[^ ]+)', ' ', text)
    text = re.sub('\{.*?\}|\[.*?\]|\=\=.*?\=\=', ' ', text)
    return text


def removeStopwords(formatted_text):
    processed_text = []
    for word in formatted_text:
        if word in stopwords:
            continue
        else:
            processed_text.append(word)
    return processed_text


def removeNonASCII(text):
    formatted_text = ''
    for char in text:
        if(ord(char) < 128):
            formatted_text += char
        else:
            formatted_text += ' '
    return formatted_text


def cleaning(text, isBody=False):
    # Lower the case
    text = text.lower()

    # Removing unwanted characters (ONLY for body text)
    if isBody:
        text = cleanBodyText(text)

    # Removing non-ASCII
    formatted_text = removeNonASCII(text)

    # Removing HTML Tags
    formatted_text = re.sub(html_tags, ' ', formatted_text)

    # Removing Special Chars
    for char in formatted_text:
        if not char.isalnum():
            formatted_text = formatted_text.replace(char, ' ')

    # Split into tokens
    formatted_text = tokenization(formatted_text)

    # Remove stopWords
    processed_text = removeStopwords(formatted_text)

    return processed_text


def stemming(processed_text):
    stemmed_text = stemmer.stemWords(processed_text)

    return stemmed_text


def processText(text, isBody=False):
    text = cleaning(text, isBody)
    text = stemming(text)
    return text


html_tags = re.compile('&amp;|&apos;|&gt;|&lt;|&nbsp;|&quot;')
stemmer = Stemmer.Stemmer('english')
stopwords = set(sw.words('english'))
