import pandas as pd
from collections import defaultdict
import ast
import csv
import  itertools

df = pd.read_csv('AuthorsYear.csv')

year_author_dict = defaultdict(list)
author_year_dict = defaultdict(list)

#first dictionary of authors and year

for index, row in df.iterrows():
    authors = ast.literal_eval(row["authors"])
    key=authors[0]['name']
    authors.pop(0)
    year=row['year']
    author_year_dict[key].append(year)

print(author_year_dict)


#second dictionary of year to authors


for index, row in df.iterrows():
    authors = ast.literal_eval(row["authors"])
    author=authors[0]['name']
    authors.pop(0)
    key=row['year']
    year_author_dict[key].append(author)

print(year_author_dict)

lengths = [len(v) for v in author_year_dict.values()]
print(min(lengths))