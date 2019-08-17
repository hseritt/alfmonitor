
#!/usr/bin/env bash

### Database choices:      ###
# sqlite3, postgresql, mysql #
DB_TYPE="postgresql"
DB_NAME="alfmonitor"

source $HOME/.bashrc
clear; reset;

echo "Clearing all *.pyc files ..."
find . -name \*.pyc -delete
echo "Done."

echo "Killing any instances of Gunicorn http server ..."
for pid in $(ps -ef | grep 'gunicorn alfmonitor.wsgi' | grep -v grep | awk '{print $2}')
do 
	kill $pid;
done
echo "Done."

echo "Killing any instances of pgadmin4 ..."
for pid in $(ps -ef | grep 'pgadmin4/pgAdmin4.py' | grep -v grep | awk '{print $2}')
do 
	kill $pid;
done
echo "Done."

if [ "$DB_TYPE" == "sqlite3" ]
then
	echo "Dropping database ..."
	rm -rf db.sqlite3
	echo "Done."
elif [ "$DB_TYPE" == "postgresql" ]
then
	echo "Dropping database ..."
	dropdb $DB_NAME
	echo "Creating database ..."
	createdb $DB_NAME -O $DB_NAME
	echo "Done."
elif [ "$DB_TYPE" == "mysql" ]
then
	mysql -u "$DB_USER" -p"$DB_PASSWD" -e "drop database $DB_NAME"
	mysql -u "$DB_USER" -p"$DB_PASSWD" -e "create database $DB_NAME"
fi

# echo "Clearing old migrations ..."
# rm -rf agents/migrations
# echo "Done."

echo "Clearing logs ..."
rm -rf logs/alfmonitor.log
rm -rf logs/gunicorn.log
echo "Done."

echo "Making migrations ..."
./manage.py makemigrations
./manage.py makemigrations agents
echo "Done."

echo "Migrating ..."
./manage.py migrate
echo "Done."

echo "Setting up admin user."
./manage.py createsuperuser --username admin --email admin@localhost --noinput
scripts/modadminpwd.py
echo "Done."

echo "Adding groups."
scripts/add_groups.py
echo "Done."

echo "Adding agent data ..."
scripts/add_agents.py
echo "Done."

echo "Adding profile data ..."
scripts/add_profiles.py
echo "Done."

echo "Setup finished."

# echo "Starting http server ..."
# echo "Control-c to stop server ..."
# ./starthttp.sh
# echo "Done."

echo "Starting http server ..."
echo "Control-c to stop server ..."
./manage.py runserver
echo "Done."

exit 0
