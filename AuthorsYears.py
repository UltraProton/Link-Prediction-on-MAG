import pandas as pd
from collections import defaultdict
import ast
import csv
import itertools

df = pd.read_csv('AuthorsYear.csv')

year_author_dict = defaultdict(list)
author_year_dict = defaultdict(list)

# first dictionary of authors and year

for index, row in df.iterrows():
    authors = ast.literal_eval(row["authors"])
    key = authors[0]['name']
    authors.pop(0)
    year = row['year']
    author_year_dict[key].append(year)

#print(author_year_dict)

# second dictionary of year to authors


for index, row in df.iterrows():
    authors = ast.literal_eval(row["authors"])
    author = authors[0]['name']
    authors.pop(0)
    key = row['year']
    year_author_dict[key].append(author)

#print(year_author_dict)

lengths = [len(v) for v in author_year_dict.values()]
# print(max(lengths))

m = 0
a = ''
for k, v in author_year_dict.items():
    if m < len(v):
        m = len(v)
        a = k

# print(a)


unipartite = defaultdict(list)

# unipartite graph for all year

for author, yearlist in author_year_dict.items():
    for year in yearlist:
        list1 = year_author_dict[int(year)]
        unipartite[author].extend(list1)

# unipartite['Huanting Chen'].pop(0)

A = unipartite['Huanting Chen'];
#print(A)

for year, authorlist in year_author_dict.items():
    if int(year) not in author_year_dict['Huanting Chen']:
        innerList = set(authorlist).intersection(A)
        if len(innerList)>0:
            print(year, innerList)

# [1996, 2013, 1994]

'''
pattern=defaultdict(list)
print(pattern)
'''

'''for key,val in unipartite.items():
    print(key,val)'''
