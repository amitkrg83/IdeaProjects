import sqlite3
from datetime import datetime, timedelta

# connect to the original database
conn_orig = sqlite3.connect('original.db')
c_orig = conn_orig.cursor()

# connect to the backup database
conn_backup = sqlite3.connect('backup.db')
c_backup = conn_backup.cursor()

# calculate the date 90 days ago
date_90_days_ago = datetime.now() - timedelta(days=90)

# query the original database to find all records older than 90 days
query = f"SELECT * FROM mytable WHERE created_at < '{date_90_days_ago.isoformat()}'"
c_orig.execute(query)

# save the results of the query to the backup database
c_backup.execute('CREATE TABLE IF NOT EXISTS mytable (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)')
for row in c_orig.fetchall():
    c_backup.execute('INSERT INTO mytable VALUES (?, ?, ?)', row)

# delete the records older than 90 days from the original database
c_orig.execute(f"DELETE FROM mytable WHERE created_at < '{date_90_days_ago.isoformat()}'")

# commit the changes to the original database
conn_orig.commit()

# close the connections to both databases
conn_orig.close()
conn_backup.close()
