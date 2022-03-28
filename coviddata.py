import spacy
from newsapi.newsapi_client import NewsApiClient
import en_core_web_lg
import pandas as pd
from collections import Counter
from string import punctuation

nlp = en_core_web_lg.load()
# used to get data from news sources
newsapi = NewsApiClient (api_key='0b52c7172d924b669f132d83a78eceb8')

articles = []
for x in range(1, 6):
    temp = newsapi.get_everything(q='coronavirus', language='en', from_param='2022-03-04', to='2022-03-24', sort_by='relevancy', page = x)
    articles.append(temp)

data = []
for a, article in enumerate(articles):
    for b in article['articles']:
        title = b['title'] # grab title
        description = b['description'] # grab description
        content = b['content'] # grab content
        data.append({'title': title, 'desc': description, 'content': content}) # add all of this info to our data list

# create dataframe
df = pd.DataFrame(data)
df = df.dropna()
df.head()

# function which takes in text parameter and gets keywords
def get_keywords_eng(content):
    result = []
    pos_tag = ['PROPN', 'VERB', 'NOUN']
    doc = nlp(content.lower())
    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return result

# list to hold results
dataResults = []
for content in df.content.values:
    dataResults.append([(x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)]) # add most common results to list
df['keywords'] = dataResults

# print this data to csv file
df.to_csv('coviddataresults.csv')
