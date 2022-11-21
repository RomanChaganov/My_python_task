import csv

file_name = input()
reader_csv = csv.reader(open(file_name, encoding='utf_8_sig'))

list_data = []
for x in reader_csv:
    list_data.append(x)

columns = list_data[0]
data = list_data[1:]

result = []
for x in data:
    if len(x) == len(columns)  and x.count('') == 0:
        result.append(x)

print(columns)
print(result)
