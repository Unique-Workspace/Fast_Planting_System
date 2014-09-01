#!/bin/bash 

log_file="./cron.log"

cd /home/pi/Workspace/Fast_Planting_System/Raspi/FastPlanting

while : 
do 
    echo "Current DIR is " $PWD 
    stillRunning=$(ps -ef |grep "$PWD/fastplanting_main.py" | grep -v "grep") 
    if [ "$stillRunning" ] ; then 
        echo "TWS service was already started by another way" 
        echo "Kill it and then startup by this shell, other wise this shell will loop out this message annoyingly" 
        kill -9 $pidof $PWD/fastplanting_main.py 
    else 
        echo "TWS service was not started" 
        echo "Starting service ..." 
        python $PWD/fastplanting_main.py >>$log_file 2>&1  # should remove  err log output in final release.
        echo "TWS service was exited at `date`" >> $log_file
    fi 
    sleep 10 
done 

