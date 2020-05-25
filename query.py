#!/usr/bin/env python3
import pandas as pd
import sqlite3
import re
from math import log
from shared import extractText, stem
from collections import defaultdict
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

#query = input()
#queryWords = [stem(w) for w in query.split()]
#print(queryWords)

# compute best query solution and output them

#tf-idf
inverted_index = pd.read_sql_query("SELECT * FROM inverted_index",conn)
idf = pd.read_sql_query("SELECT * FROM idf",conn)

metric = inverted_index.copy()
metric['tfidf'] = metric.comment * idf.values[0] + metric.multiplier * idf.values[1] \
                    + metric.comment * idf.values[2] + metric.comment * idf.values[3] 
sort_tfidf = metric.sort_values(by = ['tfidf'], ascending = False)
pd.set_option('display.max_colwidth', -1)
# %%
# tf-idf * page_rank
page_rank = pd.read_sql_query("SELECT * FROM pagerank",conn)
page_rank = page_rank[(page_rank['url'].str.contains("/A/"))]
page_rank.rename(columns = {'url':'URL'}, inplace = True)

metric_page_rank = pd.DataFrame.merge(metric, page_rank, how = 'left', on = ['URL'])
metric_page_rank['tfidf_pagerank'] = metric_page_rank.tfidf * metric_page_rank.score
sort_tfidf_pagerank = metric_page_rank.sort_values(by = ['tfidf_pagerank'], ascending = False)

#%%
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# %%
