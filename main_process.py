import subprocess
import reset_process
import data_cleaning
import create_gephi_file_formats

print('===================')
reset_process.main()
print('\n')

print('===================')
data_cleaning.main()
print('\n')

print('===================')
create_gephi_file_formats.main()
print('\n')
