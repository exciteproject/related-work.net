import os
import csv
files = os.listdir()[:-1]
ssoar = open('ssoar.csv', 'w', newline='', encoding='utf-8')
outputWriter = csv.writer(ssoar, delimiter='\t')
i = 0
for file in files:
    f = open(file, encoding='utf-8')
    for line in f:
        outputWriter.writerow([i, file.split('.')[0], line[:-1]])
        i += 1
