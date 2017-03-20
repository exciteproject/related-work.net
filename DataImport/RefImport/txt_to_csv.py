import os
import csv
files = os.listdir()[:-1]
ssoar = open('ssoar.csv', 'w', newline='', encoding='utf-8')
outputWriter = csv.writer(ssoar, delimiter='\t')
for file in files:
    f = open(file, encoding='utf-8')
    for line in f:
        outputWriter.writerow([file.split('.')[0], line[:-1]])
