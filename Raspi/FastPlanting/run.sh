#!/bin/bash 

log_file="./cron.log"

while : 
do 
    echo "Current DIR is " $PWD 
    stillRunning=$(ps -ef |grep "$PWD/loader" |grep -v "grep") 
    if [ "$stillRunning" ] ; then 
        echo "TWS service was already started by another way" 
        echo "Kill it and then startup by this shell, other wise this shell will loop out this message annoyingly" 
        kill -9 $pidof $PWD/loader 
    else 
        echo "TWS service was not started" 
        echo "Starting service ..." 
        $PWD/loader $log_file
        echo "TWS service was exited at `date`" >> $log_file
    fi 
    sleep 10 
done 

