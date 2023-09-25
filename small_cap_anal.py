import csv

with open('IWC.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
