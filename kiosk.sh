#!/bin/bash

STATUSLIST_SERVER="192.168.1.250:8001"

PID_FILE="$(dirname "${BASH_SOURCE[0]}")/kiosk.pid"
echo PID_FILE = $PID_FILE

function reload {
    # Reload page periodically
    echo Start reloading
    PID=$(cat $PID_FILE)
    kill -0 $PID
    while kill -0 $PID; do
        sleep 60
        WID=$(xdotool search --pid $PID | tail -1)
        xdotool windowactivate $WID
        xdotool key ctrl+F5
    done
}

function start {
    echo Start kiosk
    export DISPLAY=:0
    # Start chromium
    chromium-browser --kiosk $STATUSLIST_SERVER &
    PID=$!
    echo $PID > $PID_FILE
    echo Started chrommium with pid $PID
    sleep 30
    reload
}

function stop {
    echo Stop kiosk
    pkill -F $PID_FILE
    rm $PID_FILE
}


case "$1" in
    start)
        start
        exit 0
        ;;
    stop)
        stop
        exit 0
        ;;
    *)
        echo "Didn't match anything"
esac
