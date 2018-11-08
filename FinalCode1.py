import pandas as pd
from collections import defaultdict
import ast
import csv
import itertools
import numpy as np
from sklearn import metrics
import sys

csv.field_size_limit(sys.maxsize)

df = pd.read_csv('output_1.csv')

year_author_dict = defaultdict(list)
author_year_dict = {}#defaultdict(list)

for index, row in df.iterrows():
    authors = ast.literal_eval(row["authors"])
    key = authors[0]['name']
    authors.pop(0)
    year = row['year']

    if key in author_year_dict:
        inner_list=author_year_dict[key]
        if year not in inner_list:
            inner_list.append(year)
            author_year_dict[key]=inner_list

    else:
        inner_list=[]
        inner_list.append(year)
        author_year_dict[key]=inner_list


for index, row in df.iterrows():
    authors = ast.literal_eval(row["authors"])
    author = authors[0]['name']
    authors.pop(0)
    key = row['year']

    if key in year_author_dict:
        inner_list=year_author_dict[key]
        if author not in inner_list:
            inner_list.append(author)
            year_author_dict[key]=inner_list

    else:
        inner_list=[]
        inner_list.append(author)
        year_author_dict[key]=inner_list


'''
with open('author_year_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
    author_year_dict = dict((rows[0],rows[1]) for rows in reader)

print(author_year_dict)


with open('year_author_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
    year_author_dict = dict((rows[0],rows[1]) for rows in reader)

print(year_author_dict)
'''


#print(year_author_dict)

#val=10000
# first dictionary of authors and year

Ground_Truth=[]
Predicted=[]

authors_List=list(author_year_dict.keys())
#print(authors_List)
years_List=list(year_author_dict.keys())

#print(len(years_List))

for author_x in authors_List:
    input_author_yearlist = author_year_dict[author_x]

    unipartite_List=[]

    for year in input_author_yearlist:
        list1 = year_author_dict[int(year)]
        unipartite_List.extend(list1)

    list_A=author_year_dict[author_x]


    for year in years_List:

        #ground truth

        ground_truth_value=int(author_x in year_author_dict[year])
        #np.append(Ground_Truth,ground_truth_value)
        Ground_Truth.append(ground_truth_value)
        patternsList=set(year_author_dict[year]).intersection(unipartite_List)

        patterns_weight = 0
        if(len(patternsList)>0):
            degree_A = len(author_year_dict[author_x])

            for common_author in patternsList:
                degree_B = len(author_year_dict[common_author])
                degree_sum = degree_A + degree_B
                list_B = author_year_dict[common_author]

                # list of years in which author A and author B has published pupers
                common_neighbours = set(list_A).intersection(list_B)

                degree_common_neighbours = 0
                for yr in common_neighbours:
                    # Adding the degree of common neighbours i.e summation of degree of common neighbours in the formula
                    degree_common_neighbours += len(year_author_dict[yr])
                    # print(degree_common_neighbours)

                patterns_weight += (1 / (degree_common_neighbours)) * (2 / (degree_sum))

        #np.append(Predicted,patterns_weight)
        Predicted.append(patterns_weight)



ground_truth=np.array(Ground_Truth)
predicted_scores=np.array(Predicted)

#np.savetxt('Ground_Truth.csv',ground_truth,delimiter=',')
#np.savetxt('Scores.csv',predicted_scores,delimiter=',')

fpr, tpr, thresholds = metrics.roc_curve(ground_truth,predicted_scores,pos_label=1)

print(metrics.auc(fpr,tpr))

no_of_edges=0

for year , authors in year_author_dict:
    no_of_edges+=len(year_author_dict[year])



