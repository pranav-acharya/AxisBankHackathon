import scipy
import causalinference.causal as c
#from causalinference.utils import random_data
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd
from sklearn.linear_model import LogisticRegression


corpus = []
corpus.append('Flag')
dataset = []


# find corpus from single page
def get_corpus(url):
    soup = BeautifulSoup(url, "html.parser")
    corpus_link = soup.find_all("div", id="responsive-insert-ad")
    for ol in corpus_link:
        for li in ol.find_all("ol"):
            for h3 in li.find_all("h3"):
                for a in h3.find_all("a"):
                    corpus.append(a.text.replace(' ', ''))


# crawl web to make FX corpus
def crawl_corpus():
    url = urlopen('http://www.investopedia.com/categories/forex.asp').read()
    get_corpus(url)
    page = 2
    while page <= 6:
        url = urlopen('http://www.investopedia.com/categories/forex.asp?page=' + str(page)).read()
        get_corpus(url)
        page += 1


def count_word(filtered_word, count_map, word_count_set):
    i = 1
    for atr in corpus:
        if atr is 'Flag':
            continue
        if atr in filtered_word or atr.upper() in filtered_word or atr.lower() in filtered_word:
            if atr in count_map:
                count_map[atr] += count_map[atr]
            else:
                count_map.update({atr: 1})
        else:
            count_map.update({atr: 0})
        word_count_set[i] = count_map[atr]
        i += 1


def sentance_to_word(sentance):
    clean = re.sub("[^a-zA-z]", " ", sentance)
    words = clean.split()
    return words


def grab_data(url, main_url, raw_data, site_dictionary, filtered_word, hashmap):
    soup = BeautifulSoup(raw_data, "html.parser")
    # grab all links
    links = soup.find_all("a")
    for link in links:
        try:
            if link["href"].find('/') == 0:
                a = main_url + link["href"]
                if a not in hashmap and a not in site_dictionary:
                    site_dictionary.append(a)
        except KeyError:
            pass
    # grab data
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    data1 = soup.getText().replace("\n", " ")
    #nltk.download('punkt')
    #nltk.download('stopwords')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentances = tokenizer.tokenize(data1)
    word_set = []
    for sentance in sentances:
        word_set.append(sentance_to_word(sentance))
    word_set_1d = []
    for wordset in word_set:
        word_set_1d += wordset
    tokenize_word = [word for word in word_set_1d if word not in stopwords.words('english')]
    filtered_word += tokenize_word


def crawl_site(url, main_url, site_dictionary, filtered_word, hashmap):
    if hashmap.get(url) == 0:
        hashmap[url] = 1
        try:
            raw_data = urlopen(str(url)).read()
            grab_data(url, main_url, raw_data, site_dictionary, filtered_word, hashmap)
        except:
            pass
        site_dictionary.remove(url)
        #print(site_dictionary)
        if site_dictionary:
            url = site_dictionary[0]
            hashmap.update({url: 0})
            crawl_site(url, main_url, site_dictionary, filtered_word, hashmap)
    else:
        site_dictionary.remove(url)


def crawl_sites():
    file_link = pd.read_excel('/home/shailesh/Axis/linkes.csv')
    links = file_link['Links']
    files = open('/home/shailesh/Axis/sites.txt')
    file_treatment = pd.read_excel('/home/shailesh/Axis/balaji.xlsx', sheetname="Cust_list")
    del file_treatment['Customer_name']
    file_treatment['Flag'] = file_treatment['Flag'].map({'Forex': 1, 'Non Forex': 0})
    treat_data = pd.DataFrame(data=file_treatment)
    i = 0
    for site in files:
        site = site.replace("\n", '')
        site_dictionary = []
        site_dictionary.append(site)
        filtered_word = []
        hashmap = {site: 0}
        crawl_site(site, site, site_dictionary, filtered_word, hashmap)
        #print(filtered_word)
        count_map = {}
        word_count_set = [0]*len(corpus)
        word_count_set[0] = treat_data['Flag'][i]
        i += 1
        count_word(filtered_word, count_map, word_count_set)
        dataset.append(word_count_set)


def find_propensity():
    data = pd.DataFrame(dataset[1:], columns=dataset[0])
    file_name = '/home/shailesh/Axis/dataset.csv'
    data.to_csv(file_name, sep='\t', encoding='utf-8')
    read_data = pd.read_csv('/home/shailesh/Axis/dataset.csv', sep='\t')
    propensity = LogisticRegression()
    propensity = propensity.fit(read_data[corpus[1:-1]], read_data.Flag)
    pscore = propensity.predict_proba(read_data[corpus[1:-1]])[:,1]
    print(pscore)

crawl_corpus()
corpus = [x for x in corpus if x != '']
dataset.append(corpus)
crawl_sites()
find_propensity()
#file_link = pd.read_csv('/home/shailesh/Axis/links.csv')
#np.savetxt(r'/home/shailesh/Axis/sites.txt', file_link['Links'].values, fmt='%s')
