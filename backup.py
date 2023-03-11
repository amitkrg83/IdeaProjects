import sqlite3
import os
import datetime

# Set up connection to source database
source_conn = sqlite3.connect('source.db')

# Check if backup database exists
if os.path.isfile('backup.db'):
    # If backup database exists, check last backed up date
    backup_conn = sqlite3.connect('backup.db')
    cursor = backup_conn.cursor()
    cursor.execute('SELECT MAX(created_date) FROM my_table')
    last_backup_date = cursor.fetchone()[0]
    backup_conn.close()

    # Check if last backed up date is more than 90 days ago
    if (datetime.datetime.now() - datetime.datetime.strptime(last_backup_date, '%Y-%m-%d %H:%M:%S.%f')).days < 90:
        print("Last backup was less than 90 days ago. No backup needed.")
    else:
        print("Performing backup...")
        # Set up connection to backup database
        backup_conn = sqlite3.connect('backup.db')

        # Create table in backup database (if it doesn't exist)
        with backup_conn:
            backup_conn.execute('CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, name TEXT, created_date TIMESTAMP)')

        # Copy rows from source database to backup database
        with source_conn, backup_conn:
            source_conn.execute("ATTACH DATABASE 'backup.db' AS backup_db")
            source_conn.execute("INSERT INTO backup_db.my_table SELECT * FROM my_table")
            source_conn.execute("DETACH DATABASE backup_db")

        # Close connections
        backup_conn.close()
        source_conn.close()
        print("Backup complete.")

else:
    # If backup database doesn't exist, create it and copy data from source database
    print("Creating backup database...")
    backup_conn = sqlite3.connect('backup.db')

    # Create table in backup database
    with backup_conn:
        backup_conn.execute('CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, name TEXT, created_date TIMESTAMP)')

    # Copy rows from source database to backup database
    with source_conn, backup_conn:
        source_conn.execute("ATTACH DATABASE 'backup.db' AS backup_db")
        source_conn.execute("INSERT INTO backup_db.my_table SELECT * FROM my_table")
        source_conn.execute("DETACH DATABASE backup_db")

    # Close connections
    backup_conn.close()
    source_conn.close()
    print("Backup database created and populated.")
