import urllib.request
from bs4 import BeautifulSoup  # version 0.0.1
import pandas as pd  # version 2.0.2
from datetime import datetime, timedelta
import numpy as np  # version 1.23.5
from keras_preprocessing.sequence import pad_sequences  # version 1.1.2
import joblib  # version 1.2.0

# tokenizer and model upload, variable declaration whether model was changes or not
tokenizer = joblib.load('tokenizer.joblib')
model = joblib.load('model.pkl')
changed = False


def scrapper(companies):
    """
    Scraps news from first news-page of company profile on https://www.biznesradar.pl/
    :param companies: list of companies about which news are going to be scrapped
    :return: dict of news data
    """
    attributes_container = {"Company": [], "Author": [],"Headline": [], "Text": [], "Date": []}
    for company in companies:
        url_br = f'https://www.biznesradar.pl/wiadomosci/{company}'
        page_br = urllib.request.urlopen(url_br).read()
        soup_br = BeautifulSoup(page_br, 'html.parser')
        # iterating through relevant html objects
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
    """
    Filters recent news only
    parameter minutes in timedelta decide how recent news should be
    :param attributes_container: dict of news data
    :return: DataFrame of most recent news
    """
    df = pd.DataFrame(attributes_container)
    df['Date'] = pd.to_datetime(df['Date'])
    results = df[df['Date'] >= (datetime.now() - timedelta(minutes=15))]
    results.sort_values(by=['Date'], inplace=True, ascending=False)
    results.reset_index(inplace=True, drop=True)
    return results


def score_calculate(articles):
    """
    Calculate score of each news
    :param articles: DataFrame of most recent news
    :return: DataFrame of most recent news with score
    """
    articles = articles.assign(Score=lambda rows:
        [round(model.predict(j)[0][0] * 100) for j in [article_preprocessing(rows.iloc[i]) for i in range(len(rows))]])
    return articles


def print_article(article):
    """
    creates a string to put in text widget
    :param article: a single article from DataFrame
    :return: string do display
    """
    result = \
    f'Company: {article["Company"]}\n' +\
    f'Author: {article["Author"]}\n' +\
    f'Headline: {article["Headline"]}\n' +\
    f'Text: {article["Text"]}\n' + \
    f'Date: {article["Date"]}\n' +\
    f'Score: {article["Score"]} \n'
    return result


def model_actualization(score, article):
    """
    fit the model on provided article and score
    :param score: string representation of target value for given article
    :param article: single lie from DataFrame representing an article
    :return:
    """
    model_input = article_preprocessing(article)
    target = np.asarray(int(score)/100).astype('float32')
    model.fit(model_input, np.array([target]), epochs=3, verbose=0)
    # changing variable to trace model change
    global changed
    changed = True


def article_preprocessing(article):
    """
    maps article to a vector so that it would suit the model input
    :param article: single lie from DataFrame representing an article
    :return: vector of values representing an article
    """
    concat = article["Headline"] + " " + article["Text"]
    tokenized = tokenizer.texts_to_sequences([concat])
    padded = pad_sequences(tokenized, maxlen=100)
    model_input = np.asarray(padded).astype('float32')
    return model_input

