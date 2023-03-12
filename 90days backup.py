#Python script that checks if a backup database exists and if the last backup date is greater than 90 days:
#once backed up delete the data older than 90 days from the original sqlite db using python

import os
import time
import shutil
import sqlite3

# Path to SQLite database
db_path = '/path/to/sqlite.db'
# Path to backup folder
backup_folder = '/path/to/backup/folder'
# Name of backup file
backup_db_name = 'backup_db.db'

# Connect to SQLite database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Backup SQLite database
shutil.copy(db_path, os.path.join(backup_folder, backup_db_name))

# Check if backup database exists
if os.path.exists(os.path.join(backup_folder, backup_db_name)):
    # Get last modified time of backup database
    backup_time = os.path.getmtime(os.path.join(backup_folder, backup_db_name))
    # Get current time
    current_time = time.time()
    # Calculate the difference between the two times in days
    days_since_backup = (current_time - backup_time) / (24 * 60 * 60)
    # Check if the last backup date is greater than 90 days
    if days_since_backup > 90:
        print('The last backup was more than 90 days ago. Please create a new backup.')
    else:
        print('The last backup was within the last 90 days.')
        
        # Delete data older than 90 days from original SQLite database
        ninety_days_ago = time.time() - (90 * 24 * 60 * 60)
        c.execute("DELETE FROM table_name WHERE date_column < ?", (ninety_days_ago,))
        conn.commit()
        print('Data older than 90 days has been deleted from the original SQLite database.')
else:
    print('Backup database does not exist. Creating new backup...')

conn.close()
