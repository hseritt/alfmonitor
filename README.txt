Alfmonitor v0.2.0

To Start:
==============================================================================
Run ./setup.sh without --noinput and the setup script will prompt you to
create an admin username, email and password

Run ./setup.sh --noinput and an admin user will be created for you. The
username and password will be admin/admin. The email will be admin@localhost.

For demo and test purposes:

This will set up the database. Unless you have configured another database
type, server, port, database name, user and password, it will use SQLite3. 
This is NOT recommended for production or any other kind of use other than
testing.

If you're using SQLite3, this will create a flat file database called:

db.sqlite3

To reset it, simply delete the file and re-run setup.sh.

For production:

You will need to configure a database in alfmonitor/settings.py. There is a
commented section in the settings.py file that shows you how to configure a 
Postgresql database.

To reset your production database, you will need to drop it and recreate it.

Starting Alfmonitor

Once you have run ./setup.sh, you will notice a few scripts added to the
install directory.

To start Alfmonitor, issue:

# ./alfmonitor.sh start

To stop Alfmonitor, issue:

# ./alfmonitor.sh stop

Enjoy!
