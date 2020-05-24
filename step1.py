#%%
import sqlite3
import pandas as pd
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
df_webpages = pd.read_sql_query("SELECT * FROM webpages",conn)
df_responses = pd.read_sql_query("SELECT * FROM responses",conn)

print(df_webpages.head(10))
print(df_responses.head(10))
conn.commit()
conn.close()

# %%
#df_webpages.iloc[4,1]
# how many pages are indexed ? 
pd.set_option('display.max_colwidth', -1)
print(df_responses.shape)
print(df_webpages.shape)
# %%
# how many pages have the same url in request and response ?
df_responses[(df_responses['queryURL'] == df_responses['respURL'])]['queryURL'].nunique()
# %%
# why the page Surface de Delaunay is not indexed ? 
#df_webpages[df_webpages['content'].str.contains("Surface_de_Delaunay")]
#df_webpages[df_webpages['URL'].str.contains("Surface_de_Delaunay")]

#df_responses[df_responses['queryURL'].str.contains("Surface_de_Delaunay")]
df_responses[df_responses['respURL'].str.contains("Surface_de_Delaunay")]

#%%
(df_webpages['URL'].str.contains("/A/")).value_counts()
# %%
#%%
df_webpages[~(df_webpages['URL'].str.contains("/A/"))]['URL']

