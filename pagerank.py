#%%
import sqlite3
import re
from math import log
from shared import extractText, neighbors
from collections import defaultdict
import pandas as pd


NB_ITERATIONS = 50
ALPHA = 0.15

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

#compute and store pagerank
df_webpages = pd.read_sql_query("SELECT * FROM webpages",conn)
df_responses = pd.read_sql_query("SELECT * FROM responses",conn)
df_webpages = df_webpages[(df_webpages['URL'].str.contains("/A/"))]
df_webpages.rename(columns = {'URL':'queryURL'}, inplace = True)

#pointsTo = pd.merge(df_webpages, df_responses, how = 'left', on=['queryURL'])

realURL = df_responses.set_index('queryURL').T.to_dict('list')
raw_pointsTo = df_webpages.set_index('queryURL').T.to_dict('list')
pointsTo = {}

for key in raw_pointsTo:
    if key in realURL.keys():
        URL = realURL[key][0]
    else:
        URL = key
    pointsTo[URL] = raw_pointsTo[key][0]

#%%
score = {x:1/len(pointsTo) for x in pointsTo.keys()}

#%%
for i in range(50):
    new_score = {x:0.0 for x in pointsTo.keys()}
    proba_teleportation = 0.0

    for page,content in pointsTo.items():
        links = neighbors(content,page)
        links[:] = [x for x in links if "/A/" in x]
        if len(links) > 0:
            proba_teleportation += ALPHA * score[page]
            for link in links:
                link = realURL[link][0]
                new_score[link] += score[page] * (1-ALPHA)/len(links)
        else:
            proba_teleportation += score[page]
    for page in pointsTo:
        new_score[page] += proba_teleportation/len(pointsTo)
    score = new_score.copy()
#%%
i = 1
for p in sorted(score, key=score.get, reverse=True):
    i += 1 
    print(p, score[p])
    if i > 20:
        break
conn.commit()
print('ok')


# %%
