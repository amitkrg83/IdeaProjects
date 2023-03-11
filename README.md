# IdeaProjects

In this script, we first connect to the source database (source.db). We then check if the backup database file (backup.db) exists. If it does, we connect to it and use a query to get the maximum created date from the my_table table. We then calculate the number of days between the last backed up date and today's date. If the number of days is less than 90, we print a message indicating that no backup is needed. If the number of days is greater than or equal to 90, we proceed with the backup process.

If the backup database file doesn't exist, we create it and copy the data from the source database into it.

Note that you will need to replace source.db with the filename of your source database, backup.db with the filename you want to use for your backup database, my_table with the name of the table in your database that you want to back up, and created_date with the name of the column in your table that contains timestamps for when each row was created.
