#create a copy of sqlite db into another folder using python

import shutil

# Set the paths of the original database and the copy
original_path = "/path/to/original/database.db"
copy_path = "/path/to/new/folder/copy.db"

# Copy the database file to the new folder
shutil.copyfile(original_path, copy_path)

print("Database copy created at", copy_path)