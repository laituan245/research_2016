import os
import csv

print 'Start to execute code in ' + os.path.basename(__file__)

PREPROCESSED_DATA_DIRECTORY = 'Preprocessed data'
PREPROCESSED_DATA_FILENAME = 'preprocessed_dblp.txt'
ID_TITLE_MAPPINGS_FILENAME = 'id_title_mappings.txt'
GEPHI_DATA_DIRECTORY = 'Gephi data'
GEPHI_NODE_DATA_FILENAME = 'Nodes1.csv'
GEPHI_EDGE_DATA_FILENAME = 'Edges1.csv'
# We will consider only the years from 1980 to 2015
YEAR_MIN = 1980
YEAR_MAX = 2015

def remove_special_chars(my_string):
    # Replace all special characters by the underscore characters
    rs = ''
    for e in my_string:
        if e.isalnum():
            rs = rs + e
        else:
            rs = rs + '_'
    return rs

if not os.path.exists(GEPHI_DATA_DIRECTORY):
    os.makedirs(GEPHI_DATA_DIRECTORY)

nodes = {}

titles = []
ids = []
cnt = 0
f = open(PREPROCESSED_DATA_DIRECTORY + '/' + ID_TITLE_MAPPINGS_FILENAME, 'r')
for line in f:
    if '#*' in line:
        cnt += 1
        titles.append(line.strip()[2:].lower())
    elif '#index' in line:
        ids.append(line.strip()[6:].lower())
assert(cnt == 3272991)
for i in range(cnt):
    if not ids[i] in nodes:
        nodes[ids[i]] = {'titles': [], 'year': -1}
    nodes[ids[i]]['titles'].append(titles[i])
f.close()
print 'Done getting data from the file ' + ID_TITLE_MAPPINGS_FILENAME

cnt = 0
cur_id = 'None'; cur_year = -1;
years = []
f = open(PREPROCESSED_DATA_DIRECTORY + '/' + PREPROCESSED_DATA_FILENAME, 'r')
for line in f:
    if '#index' in line:
        cnt += 1
        cur_id = line.strip()[6:]
    elif '#t' in line:
        cur_year = int(line.strip()[2:])
        years.append(cur_year)
    elif '#%' in line:
        pass
    else:
        nodes[cur_id]['year'] = cur_year
assert(cnt == 3272991)
f.close()
years = list(set(years))
years.sort()
print 'The list of years is: ' + str(years)
print 'Done getting data from the file ' + PREPROCESSED_DATA_FILENAME

with open(GEPHI_DATA_DIRECTORY + '/' + GEPHI_NODE_DATA_FILENAME, 'w+') as csvfile:
    fieldnames = ['Id', 'Label', 'Timeset']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for cur_id in nodes.keys():
        my_year = nodes[cur_id]['year']
        if my_year >= YEAR_MIN and my_year <= YEAR_MAX:
            writer.writerow({'Id': cur_id,
                             'Label': remove_special_chars(nodes[cur_id]['titles'][0]),
                             'Timeset': '<[' + str(my_year) + ', ' + str(YEAR_MAX) + ']>'})
print 'Done creating the file ' + GEPHI_NODE_DATA_FILENAME

with open(GEPHI_DATA_DIRECTORY + '/' + GEPHI_EDGE_DATA_FILENAME, 'w+') as csvfile:
    fieldnames = ['Source', 'Target', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    f = open(PREPROCESSED_DATA_DIRECTORY + '/' + PREPROCESSED_DATA_FILENAME, 'r')
    cur_id = 'None'
    for line in f:
        if '#index' in line:
            cur_id = line.strip()[6:]
        elif '#t' in line:
            pass
        elif '#%' in line:
            target_id = line.strip()[2:]
            cur_year = nodes[cur_id]['year']
            target_year = nodes[target_id]['year']
            if (cur_year >= YEAR_MIN and cur_year <= YEAR_MAX):
                if (target_year >= YEAR_MIN and target_year <= YEAR_MAX):
                    writer.writerow({'Source': cur_id,
                                     'Target': target_id,
                                     'Type': 'Directed'})

    f.close()
print 'Done creating the file ' + GEPHI_EDGE_DATA_FILENAME
