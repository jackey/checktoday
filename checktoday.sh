#!/usr/bin/env bash

PATH=/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:
DAEMON=$PWD/checktoday.py
PID=$PWD/.pid

test -f $PID || echo "" > $PID

test -x $DAEMON || exit 0

. /lib/lsb/init-functions

case "$1" in
	start)
		log_daemon_msg "Starting checktoday"
		start_daemon -p $PID $DAEMON
		log_end_msg $?
		;;
	stop)
		log_daemon_msg "Stoping checktoday"
		killproc -p $PID $DAEMON
		PID = ` ps x | grep checktoday | head -1 | awk '{print $1}'`
		kill -9 $PID
		log_end_msg $?
		;;
	restart)
		$0 stop
		$o start
		;;
	*)
		echo "Usage: run.sh start | stop | restart "
		exit 1
		;;
esac

exit 0
