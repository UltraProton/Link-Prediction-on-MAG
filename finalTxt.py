import csv, json
import os
import glob


#path0='/media/sunil/8C62C9A162C9907E/DataBaseOFDB/demo/*.txt'
#path0='/CS18MTECH11039/mag_papers_0/*.txt'
filelist=['mag_papers_0.txt','mag_papers_1.txt','mag_papers_2.txt','mag_papers_3.txt','mag_papers_4.txt','mag_papers_5.txt',
          'mag_papers_6.txt','mag_papers_7.txt','mag_papers_8.txt','mag_papers_9.txt','mag_papers_10.txt','mag_papers_11.txt','mag_papers_12.txt',
          'mag_papers_13.txt','mag_papers_14.txt','mag_papers_15.txt',
          'mag_papers_16.txt','mag_papers_17.txt','mag_papers_18.txt','mag_papers_19.txt']
#path1='/media/sunil/8C62C9A162C9907E/DataBaseOFDB/demo/final.txt'
path1='final.txt'
with open(path1, 'w') as outfile:
    for filename in filelist:
        with open(filename) as infile:

            for line in infile:
                outfile.write(line)


all_fields = ['id','title','authors','year','keywords','fos','n_citation','references',
              'doc_type','lang','publisher','isbn','doi','pdf','volume', 'issue', 'venue','page_start','page_end']

with open("FINAL_OUTPUT.csv", "w") as output_file:
    writer = csv.DictWriter(output_file,all_fields)
    writer.writeheader()


    input = []

    for line in open(path1, 'r'):
        if line.strip():
            input.append(json.loads(line))


    for row in input:

        if 'abstract' in row: del row['abstract']

        if 'url' in row: del row['url']

        '''if 'authors' in row:
            #print(row['authors'][0]['name'])
            innDict=row['authors']
            for line in innDict:
                print(line)
                if 'name' in line:row['author_name']=line['name']
                if 'org' in line: row['author_org'] = line['org']
            del row['authors']'''



    for row in input:
        writer.writerow(row)