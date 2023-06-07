import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import pyarrow.feather as feather  # version 12.0.0

# TODO: compaies from wig20
companies = ['PLAYWAY', "LPP", "GPW", "KGHM", "DINOPL"]
attributes_container = {"Company": [], "Author": [], "Headline": [], "Text": [], "Date": []}
for company in companies:
    for page in range(1, 11):
        url_br = f'https://www.biznesradar.pl/wiadomosci/{company},{page}'
        page_br = urllib.request.urlopen(url_br).read()
        soup_br = BeautifulSoup(page_br, 'html.parser')
        for elem in soup_br.find_all(['div', 'span']):
            if elem.name == 'div':
                try:
                    if elem['class'] == ['record-header']:
                        attributes_container['Headline'].append(elem.contents[1].string)
                        attributes_container['Company'].append(company)
                    elif elem['class'] == ['record-body']:
                        attributes_container['Text'].append(elem.string)
                    elif elem['class'] == ['record-footer']:
                        if elem.contents[1]['class'] == ['record-author']:
                            attributes_container['Author'].append(elem.contents[1].string)
                        else:
                            attributes_container['Author'].append('NA')
                except KeyError:
                    continue
            # TODO: get 'span' to div
            elif elem.name == 'span':
                try:
                    if elem['class'] == ['record-date']:
                        attributes_container['Date'].append(elem.string)
                except KeyError:
                    continue

df = pd.DataFrame(attributes_container)
feather.write_feather(df, 'news.arrow')
