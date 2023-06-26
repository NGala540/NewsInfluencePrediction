import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup  # version 0.0.1
import pandas as pd  # version 2.0.2
import pyarrow.feather as feather  # version 12.0.0

while True:
    chosen_set = int(input("Choose set to scrapp (1 or 2): "))
    if chosen_set == 1 or chosen_set == 2:
        break

companies_set_1 = ['ASSECO-POLAND', "ALE", "ALIOR-BANK", "CD-PROJEKT", "CYFROWY-POLSAT",
                   "DNP", "JSW-JASTRZEBSKA-SPOLKA-WEGLOWA", "KGHM", "KRUK", "KETY"]
companies_set_2 = ["LPP", "MBANK", "ORANGE", "PCO", "PEKAO",
                   "PGE", "PKN-ORLEN", "PKO", "PZU", "SPL"]

attributes_container = {"Company": [], "Author": [], "Headline": [], "Text": [], "Date": []}
for company in companies_set_1 if chosen_set == 1 else companies_set_2:
    for page in range(1, 16):
        url_br = f'https://www.biznesradar.pl/wiadomosci/{company},{page}'
        try:
            page_br = urllib.request.urlopen(url_br).read()
        except HTTPError:
            print(f"page {page} not found")
            break
        soup_br = BeautifulSoup(page_br, 'html.parser')
        for elem in soup_br.find_all(['div', 'span']):
            if elem.name == 'div':
                try:
                    if elem['class'] == ['record-header']:
                        attributes_container['Headline'].append(elem.contents[1].string)
                        attributes_container['Company'].append(company)
                    elif elem['class'] == ['record-body']:
                        attributes_container['Text'].append(elem.string.replace("\n", "").replace("\t", ""))
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
        print(f"page no. {page} for {company} scrapped")

df = pd.DataFrame(attributes_container)
feather.write_feather(df, f'news{chosen_set}.arrow')
