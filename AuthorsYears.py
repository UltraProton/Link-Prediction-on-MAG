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

print("Enter the name of author: ")
Input_author=input()

A = unipartite['Huanting Chen'];
#print(A)

pattern_dict=defaultdict(list)

#It creates the unipartite graph of authors
for year, authorlist in year_author_dict.items():
    if int(year) not in author_year_dict[Input_author]:
        innerList = set(authorlist).intersection(A)
        if len(innerList)>0:
        #    print(year, innerList)
            pattern_dict[year].append(innerList)

degree_A=len(author_year_dict[Input_author])

for year , authors in pattern_dict.items():
    for author in authors:
        degree_B=len(author_year_dict[author])
        degree_sum=degree_A+degree_B
        list_A=author_year_dict[Input_author]
        list_B=author_year_dict[author]
        common_neighbours=set(list_A).intersection(list_B)

        degree_common_neighbours=0
        for yr in common_neighbours:
            degree_common_neighbours+=len(year_author_dict[yr])

        pattern_weight=(1/(degree_common_neighbours))*(2/(degree_sum))

    break






# [1996, 2013, 1994]

'''
pattern=defaultdict(list)
print(pattern)
'''

'''for key,val in unipartite.items():
    print(key,val)'''
