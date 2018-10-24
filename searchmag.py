import pandas as pd
import csv
import pandas

df = pd.read_csv('FINAL_OUTPUT.csv')


venues = {}
for line in open('dblpjournals.txt', 'r'):
    line = line.strip()
    line = line.rstrip('\n')
    line = line.lstrip()
    line = line.lower()
    venues[line] = line

all_fields = ['authors']
with open("Authors2.csv", "w") as output_file:
    writer = csv.DictWriter(output_file, all_fields)
    writer.writeheader()

    for index, row in df.iterrows():
        venue = row['venue']
        if pandas.isnull(venue) or pandas.isnull(row['authors']):
            continue

        venue = venue.lower()

        if venue in venues:

            writer.writerow({'authors':row['authors']})
