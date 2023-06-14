import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from keras_preprocessing.sequence import pad_sequences

def scrapper(companies):
    attributes_container = {"Company": [], "Author": [], "Headline": [], "Text": [], "Date": []}
    for company in companies:
        url_br = f'https://www.biznesradar.pl/wiadomosci/{company}'
        page_br = urllib.request.urlopen(url_br).read()
        soup_br = BeautifulSoup(page_br, 'html.parser')
        for elem in soup_br.find_all(['div', 'span']):
            if elem.name == 'div':
                try:
                    if elem['class'] == ['record-header']:
                        attributes_container['Headline'].append(elem.contents[1].string)
                        attributes_container['Company'].append(company)
                    elif elem['class'] == ['record-body']:
                        attributes_container['Text'].append(elem.string.replace("\n", "").replace("\t", "").lstrip())
                    elif elem['class'] == ['record-footer']:
                        if elem.contents[1]['class'] == ['record-author']:
                            attributes_container['Author'].append(elem.contents[1].string)
                        else:
                            attributes_container['Author'].append('NA')
                except KeyError:
                    continue
            elif elem.name == 'span':
                try:
                    if elem['class'] == ['record-date']:
                        attributes_container['Date'].append(elem.string)
                except KeyError:
                    continue

    return attributes_container


def is_current(attributes_container):
    results = []
    df = pd.DataFrame(attributes_container)
    df['Date'] = pd.to_datetime(df['Date'])
    # TODO: Iterating through pandas objects is generally slow. In many cases, iterating manually over the rows is not needed
    for index, row in df.iterrows():
        if row['Date'] >= datetime.now() - timedelta(minutes=90):
            results.append(row)

    return results

def print_article(article, model, tokenizer):
    corpus = input_processor(str(article[2]), str(article[3]), tokenizer)
    result = \
    f'Company: {str(article[0])}\n' +\
    f'Author: {str(article[1])}\n' +\
    f'Headline: {str(article[2])}\n' +\
    f'Text: {str(article[3])}\n' +\
    f'Date: {str(article[4])}\n' +\
    f'Score: {round(model.predict([corpus])[0][0] * 100)} \n'
    return result

def input_processor(head, body, tokenizer):
    concat = head + " " + body
    tokenized = tokenizer.texts_to_sequences([concat])
    padded = pad_sequences(tokenized, maxlen=100)
    result = np.asarray(padded).astype('float32')
    return result
