#!/usr/bin/env bash

opt=$1

source $HOME/.bashrc

# User configurable variables:
PYTHON="python"
BIND_IP="127.0.0.1"
ALFM_ENGINE="-m engine"
START_HTTPSVC="starthttp.sh"
HTTPSVC="alfmonitor.wsgi"
MONITOR="monitor.py"

# Commands. Don't change these unless you know what you're doing.
START_ENGINE="$PYTHON $ALFM_ENGINE"

# Messages
DUPLICATE_PROC_MSG="Another instance of alfmonitor engine is already running."
DUPLICATE_HTTP_MSG="Another instance of alfmonitor http is already running."
SHUTDOWN_MSG="Shutting down Alfmonitor:"
ENGINE_SHUTDOWN_MSG="  * alfmonitor engine Done"
GUNICORN_SHUTDOWN_MSG="  * gunicorn process Done"
HTTP_SHUTDOWN_MSG="  * http Done"
MONITOR_SHUTDOWN_MSG="  * monitor Done"
ALF_MONITOR_COMPLETE_SHUTDOWN="Alfmonitor shut down."
KILL_WAIT=1
GUNICORN_KILL_WAIT=5

# Usage print out.
function usage {
	echo ""
	echo " alfmonitor.sh - Script to start Alfmonitor and web console."
	echo "Usage: "
	echo "	alfmonitor.sh [start|stop]"
	echo ""
	exit
}

function shut_down {
	pid=$1
	msg=$2
	kill $pid 2>/dev/null
	sleep $KILL_WAIT
	echo "$msg"
}

# Start #
if [ "$opt" == "" ]
then
	usage;
fi

if [ "$opt" == "start" ]
then
	count=$(ps -ef | grep "$START_ENGINE" | grep -v grep | wc -l)

	if [ "$count" == 0 ]
	then
		echo "Starting Alfmonitor engine ..."
		$START_ENGINE &
	else
		echo "$DUPLICATE_PROC_MSG"
	fi

	count=$(ps -ef | grep $START_HTTPSVC | grep -v grep | wc -l)

	if [ "$count" == 0 ]
	then
		./$START_HTTPSVC &
	else
		echo "$DUPLICATE_HTTP_MSG"
	fi
fi

if [ "$opt" == "stop" ]
then
	echo "$SHUTDOWN_MSG"
	for pid in $(ps -ef|grep "$START_ENGINE"|grep -v grep| awk '{print $2}')
	do
		shut_down $pid "$ENGINE_SHUTDOWN_MSG"
	done
	
	for pid in $(ps -ef|grep "$MONITOR" |grep -v grep| awk '{print $2}')
	do
		shut_down $pid "$MONITOR_SHUTDOWN_MSG"
	done

	for pid in $(ps -ef|grep "$START_HTTPSVC" |grep -v grep| awk '{print $2}')
	do
		shut_down $pid "$HTTP_SHUTDOWN_MSG"
	done

	for pid in $(ps -ef|grep "$HTTPSVC" | grep "gunicorn" | grep -v grep| awk '{print $2}')
	do
		shut_down $pid "$GUNICORN_SHUTDOWN_MSG"
		sleep $GUNICORN_KILL_WAIT
	done

	echo "$ALF_MONITOR_COMPLETE_SHUTDOWN"
fi

exit 0
