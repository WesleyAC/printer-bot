#!/bin/sh
while [ 1 ]
do
        echo "Starting printer bot!"
        python3 printer-bot.py &
        sleep 30m
        echo "Killing printer bot </3"
        kill $(ps au | grep printer-bot | head -n1 | awk '{ print $2 }')
done
