#!/bin/bash
#
# This seems to be necessary to force the runner to pickup queued jobs.
# It just hangs around in IDLE otherwise... This seems to be encountered
# by others using self-hosted runners.
#

set -e

LOG_FILE=/home/runner/runner.log

if [ ! -f $LOG_FILE ]; then
    echo "Logfile does not exist: $LOG_FILE. Exiting."
    exit 1
fi

function start_runner {
    cd /home/runner/actions-runner
    rm $LOG_FILE
    echo "" > $LOG_FILE
    sleep 5
    nohup ./run.sh > $LOG_FILE 2>&1 &
}

if tail -n 1 "$LOG_FILE" | grep -qE "Job.*completed|Listening for Jobs"; then
    echo "Runner is idle. Restarting"
    pid=$(ps ux | awk '/\/home\/runner\/actions-runner\/bin\/Runner.Listener run/ && !/awk/ {print $2}')
    kill $pid
    start_runner
elif ! ps ux | grep -q "[R]unner.Listener"; then
    echo "Runner not running. Starting"
    start_runner
else
    echo "Runner is executing a job. Nothing done."
fi
