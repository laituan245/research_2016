import os
import shutil

def main():
    print 'Start to execute code in ' + os.path.basename(__file__)

    RAW_DATA_DIRECTORY = 'Raw data'
    PREPROCESSED_DATA_DIRECTORY = 'Preprocessed data'
    GEPHI_DATA_DIRECTORY = 'Gephi data'
    RAW_DATA_FILENAME = 'dblp.txt'

    # Let's remove all the intermediate files/folders (if any)
    if os.path.exists(RAW_DATA_DIRECTORY):
        if os.path.isfile(RAW_DATA_DIRECTORY + '/' + RAW_DATA_FILENAME):
            os.remove(RAW_DATA_DIRECTORY + '/' + RAW_DATA_FILENAME)

    if os.path.exists(PREPROCESSED_DATA_DIRECTORY):
        shutil.rmtree(PREPROCESSED_DATA_DIRECTORY, ignore_errors=True)

    if os.path.exists(GEPHI_DATA_DIRECTORY):
        shutil.rmtree(GEPHI_DATA_DIRECTORY, ignore_errors=True)

if __name__ == "__main__":
    main()
