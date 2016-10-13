import os

RAW_DATA_DIRECTORY = 'Raw data'
RAW_DATA_FILENAME = 'dblp.txt'
PREPROCESSED_DATA_DIRECTORY = 'Preprocessed data'
PREPROCESSED_DATA_FILENAME = 'preprocessed_dblp.txt'

if not os.path.exists(PREPROCESSED_DATA_DIRECTORY):
    os.makedirs(PREPROCESSED_DATA_DIRECTORY)

# Let's do a sanity check. The raw dataset should have 3,272,991 papers
# and 8,466,859 citation relationships
nb_papers = 0
nb_citation_rels = 0
f = open(RAW_DATA_DIRECTORY + '/' + RAW_DATA_FILENAME, 'r')
for line in f:
    nb_papers += (1 if '#*' in line else 0)
    nb_citation_rels += (1 if '#%' in line else 0)
assert (nb_papers == 3272991)
assert (nb_citation_rels == 8466859)
print 'The sanity check was completed'

# Let's remove unnecessary information from the raw dataset.
raw_file = open(RAW_DATA_DIRECTORY + '/' + RAW_DATA_FILENAME, 'r')
new_file = open(PREPROCESSED_DATA_DIRECTORY + '/' + PREPROCESSED_DATA_FILENAME, 'w+')
for line in raw_file:
    is_unnecessary = False
    if '#*' in line:
        # We don't need the info about the title (at least for now)
        is_unnecessary = True
    if '#@' in line:
        # We don't need the info about the author (at least for now)
        is_unnecessary = True
    if '#!' in line:
        # We don't need the info about the abstract (at least for now)
        is_unnecessary = True
    if '#c' in line:
        # We don't need the info about the publication venue
        is_unnecessary = True
    if not is_unnecessary:
        new_file.write(line)
print 'Removed unnecessary information from the raw dataset.'
print 'Created a new file ' + PREPROCESSED_DATA_FILENAME
