import pandas as pd
from collections import defaultdict
import ast
import csv
import itertools
import numpy as np
from sklearn import metrics
import sys

csv.field_size_limit(sys.maxsize)

#records filename and corresponding AUC value
file_AUC_dict={}

#list to store the name of files for which AUC score will be calculated
record_files_names=[]

#store the name of the files to run algorithm on
for i in range(1,6):
    record_files_names.append("output_"+str(i)+".csv")

#To append the name of a file with appropriate no
file_number=1

#Run algorithm on every file in record file names
for records_file_name in record_files_names:
    file_name=records_file_name
    df = pd.read_csv(file_name)

#Dictionaries to store bipartite graph
    year_author_dict = defaultdict(list)
    author_year_dict = {}#defaultdict(list)

#creating author to year links
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


#Creating year to author links
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

#Ground Truth values for each record of author and year to be stored in Ground_Truth=[]
    Ground_Truth=[]
#Predicted link scores for each record
    Predicted=[]

#List of all the authors
    authors_List=list(author_year_dict.keys())
    #print(authors_List)
#list of all the years
    years_List=list(year_author_dict.keys())

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
            innerList=set(year_author_dict[year]).intersection(unipartite_List)

            patterns_weight = 0
            if(len(innerList)>0):
                degree_A = len(author_year_dict[author_x])

                for common_author in innerList:
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

    #np.savetxt('Ground_Truth'+str(file_number)+'.csv',ground_truth,delimiter=',')
    #np.savetxt('Scores'+str(file_number)+'.csv',predicted_scores,delimiter=',')

    fpr, tpr, thresholds = metrics.roc_curve(ground_truth,predicted_scores,pos_label=1)

    auc_value=metrics.auc(fpr,tpr)

    file_AUC_dict[file_name]=auc_value

with open('file_AUC_value.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in file_AUC_dict.items():
       writer.writerow([key, value])



