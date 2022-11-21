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
    if len(x) == len(columns) and x.count('') == 0:
        result.append(x)

def delete_tag(string):
    start_position = string.find('<')
    end_position = string.find('>')
    if start_position == -1 or end_position == -1:
        return string
    return delete_tag(string[:start_position] + string[end_position + 1 : len(string)])

senteces = {}
resumes = []
for i in range(len(result)):
    for j in range(len(columns)):
        result[i][j] = ', '.join(result[i][j].split('\n'))
        result[i][j] = delete_tag(result[i][j])
        result[i][j] = ' '.join(result[i][j].split())
        senteces[columns[j]] = result[i][j]
    resumes.append(senteces.copy())

for sentence in resumes:
    for key, value in sentence.items():
        print(f'{key}: {value}')
    print()
