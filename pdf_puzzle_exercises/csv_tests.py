import csv
import PyPDF2

data = open('example.csv',encoding="utf-8")
#print (data)

csv_data = csv.reader(data)
#print (csv_data)
data_lines=list (csv_data)
for line in data_lines[:5]:
    print(line)

all_emails=[]
for line in data_lines:
    print(line[3])

