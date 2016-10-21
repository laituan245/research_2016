import os
import csv
from random import randint

RAW_DATA_DIRECTORY = 'Raw data'
RAW_DATA_FILENAME = 'dblp.txt'
GEPHI_DATA_DIRECTORY = 'Gephi data'
GEPHI_NODE_DATA_FILENAME = 'Nodes1.csv'
GEPHI_EDGE_DATA_FILENAME = 'Edges1.csv'
# We will consider only the years from 1980 to 2015
YEAR_MIN = 1980
YEAR_MAX = 2015

def remove_special_chars(my_string):
    # Replace all special characters
    rs = ''
    for e in my_string:
        if e.isalnum():
            rs = rs + e
    return rs

def random_testing(random_nb):
    my_node = {}
    with open(os.path.dirname(__file__) + '/../' + GEPHI_DATA_DIRECTORY + '/' + GEPHI_NODE_DATA_FILENAME, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        cnt = 0
        for row in reader:
            if (cnt == random_nb):
                my_node['Id'] = row[0].strip()
                my_node['Label'] = remove_special_chars(row[1].strip())
                timeset = row[2][2:-2]
                my_node['start_year'] = int(timeset.split(',')[0])
                my_node['end_year'] = int(timeset.split(',')[1])
                my_node['in_nodes'] = []
                my_node['out_nodes'] = []
                break
            cnt = cnt + 1

    with open(os.path.dirname(__file__) + '/../' + GEPHI_DATA_DIRECTORY + '/' + GEPHI_EDGE_DATA_FILENAME, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        first_line = True
        for row in reader:
            if first_line:
                first_line = False
            else:
                if row[0].strip() == my_node['Id']:
                    my_node['out_nodes'].append(row[1])
                elif row[1].strip() == my_node['Id']:
                    my_node['in_nodes'].append(row[0])
    my_node['out_nodes'] = list(set(my_node['out_nodes']))
    my_node['in_nodes'] = list(set(my_node['in_nodes']))
    my_node['out_nodes'].sort()
    my_node['in_nodes'].sort()

    raw_file = open(os.path.dirname(__file__) + '/../' + RAW_DATA_DIRECTORY + '/' + RAW_DATA_FILENAME, 'r')
    cur_id = 'None'; cur_year = -1; cur_title = 'None'; pub_list = [];
    expected_year = -1; expected_titles = []; expected_out_nodes_list = [];
    expected_in_nodes_list = []
    for line in raw_file:
        line = line.strip()
        if line.startswith('#index'):
            cur_id = line[6:]
        elif line.startswith('#t'):
            cur_year = int(line[2:])
        elif line.startswith('#*'):
            cur_title = remove_special_chars(line.lower())
        elif line.startswith('#%'):
            pub_list.append(line[2:])
            if line[2:].strip() == my_node['Id']:
                expected_in_nodes_list.append(cur_id)
        elif len(line) == 0:
            if cur_id == my_node['Id']:
                expected_year = cur_year
                expected_titles.append(cur_title)
                expected_out_nodes_list += pub_list
            cur_id = 'None'; cur_year = -1; cur_title = 'None'; pub_list = [];
    raw_file.close()

    expected_out_nodes_list = list(set(expected_out_nodes_list))
    expected_out_nodes_list.sort()
    expected_in_nodes_list = list(set(expected_in_nodes_list))
    expected_in_nodes_list.sort()

    print 'Total degree = ' + str(len(my_node['in_nodes']) + len(my_node['out_nodes']))
    assert(my_node['out_nodes'] == expected_out_nodes_list)
    assert(my_node['in_nodes'] == expected_in_nodes_list)
    assert(my_node['Label'] in expected_titles)
    assert(my_node['start_year'] == expected_year)
    assert(my_node['end_year'] == YEAR_MAX)

def main():
    nb_nodes_considered = 0
    with open(os.path.dirname(__file__) + '/../' + GEPHI_DATA_DIRECTORY + '/' + GEPHI_NODE_DATA_FILENAME, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            nb_nodes_considered = nb_nodes_considered + 1
        nb_nodes_considered -= 1 # The first row is the header row

    nb_random_tests = 100
    print 'About to conduct ' + str(nb_random_tests) + ' random tests'
    for i in range(nb_random_tests):
        print '==================='
        print 'Started the random test ' + str(i+1)
        random_nb = randint(1, nb_nodes_considered)
        print 'random_nb = ' + str(random_nb)
        random_testing(random_nb)
        print 'Passed the random ' + str(i+1)
        print '\n'

if __name__ == "__main__":
    main()
