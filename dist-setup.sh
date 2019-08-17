#!/usr/bin/env bash

ALFM_VERSION="0.0.3"
python="$HOME/.pyenv/shims/python"

function show_usage {
	echo "Alfmonitor $ALFM_VERSION Setup"
	echo "Usage:"
	echo "./setup.sh [--noinput | --upgrade |]"
	echo ""
	echo "--noinput : Console admin user will be created for you."
	echo "--upgrade : Console admin user creation will be skipped."
	echo ""
	exit 0
}

echo "Alfmonitor ${ALFM_VERSION} Setup"
sleep 2

echo "Installing Python packages ..."
$HOME/.pyenv/shims/pip install -r requirements.txt

mv scripts/manage.py . 2>/dev/null

echo "Alfmonitor v${ALFM_VERSION} - May 2018"
sleep 1
echo "Setting up the database ..."
sleep 1

$python manage.py makemigrations
$python manage.py migrate
echo "Database setup complete."


echo ""

if [ "$1" == "--noinput" ]
then
	sleep 1
	echo "The console admin user will be created automatically for you."
	echo "Remember these:"
	echo "username: admin"
	echo "password: admin"
	sleep 2
	$python manage.py createsuperuser --noinput --username admin --email admin@localhost 2>/dev/null
	$python scripts/modadminpwd.py
elif [ "$1" == "--upgrade" ]
then
	echo "Upgrade being performed."
	echo "Console admin user creation will be skipped."
	echo "Running schema updates on existing database."
	$python scripts/updatedb.py
	sleep 3
else
	echo "Next, you will be asked to create an admin user."
	sleep 2
	echo "Make sure you remember your username and password."
	$python manage.py createsuperuser
fi

sleep 3

echo "Adding groups."
scripts/add_groups.py
echo "Done."

mv scripts/alfmonitor.sh . 2>/dev/null
mv scripts/engine.pyc . 2>/dev/null
mv scripts/monitor.pyc . 2>/dev/null
mv scripts/starthttp.sh . 2>/dev/null

echo "Setting up out of the box agents ..."
$python scripts/add_agents.py
echo "Done."

echo "Setup complete."
echo "To start Alfmonitor, run: ./alfmonitor.sh start"
echo "To stop Alfmonitor, run: ./alfmonitor.sh stop"
echo "To view the Alfmonitor Console, point your browser to: "
echo "http://localhost:8000"
echo ""
echo "Enjoy!"
