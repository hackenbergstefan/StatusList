#!/usr/bin/bash

PID_FILE="$(dirname "${BASH_SOURCE[0]}")/kiosk.pid"

function start {
    sleep 10
    chromium-browser --enable-fullscreen --kiosk "localhost:8001" &
    echo $! > kiosk.pid
}

function stop {
    pkill $(cat kiosk.pid)
}


case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
        echo "Didn't match anything"
esac
