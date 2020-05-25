#!/usr/bin/env python3
#%%
import sqlite3
import re
from math import log
from shared import extractListOfWords, stem
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from collections import Counter

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# compute the inverted index and the idf and store them
# input: list L of words, output: list of (w,f) 

L = ['comment','multiplier','des','matrice']

df_webpages = pd.read_sql_query("SELECT * FROM webpages",conn)
df_webpages = df_webpages[(df_webpages['URL'].str.contains("/A/"))]

def countFreq(L, corpus):
    L_stemmed = [stem(i) for i in L]
    cnt = Counter()
    for word in corpus:
        cnt[word] += 1

    tf = []
    for word in L_stemmed:
        if len(corpus) == 0 :
            f = 0
        else:  
            f = cnt[word]/len(corpus)
        tf.append((word, f))
    return tf   
 
#pages = df_webpages['content'].values
columns = ['URL']
columns.extend(L)
result = pd.DataFrame(columns=columns)
result['URL'] = None
for i, row in df_webpages.iterrows():
    page = row['content']
    corpus = [stem(i) for i in extractListOfWords(page)]
    tf = countFreq(L,corpus)
    temp = [row['URL']]
    temp.extend([t[1] for t in tf])
    temp = pd.Series(temp).to_frame(0).T
    temp.columns = columns
    result = result.append(temp)

idf = {}
for word in L:
    idf[word] = log(len(result)/sum(result[word]>0))

idf = pd.DataFrame.from_dict(idf,orient='index')

conn.execute("DROP TABLE IF EXISTS inverted_index")
result.to_sql('inverted_index', conn, if_exists='replace', index=False)

conn.execute("DROP TABLE IF EXISTS idf")
idf.to_sql('idf', conn, if_exists='replace', index=False)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
