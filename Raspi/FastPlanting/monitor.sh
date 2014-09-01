#!/bin/bash

if [ -z "$1" -o -z "$2" ]
then
    echo "Usage: ./monitor.sh <user_name> <process_name>"
    exit
fi

PsUser=$1
PsName=$2
pid=`ps -u $PsUser|grep $PsName|grep -v grep|grep -v vi|grep -v dbx |grep -v tail|grep -v start|grep -v stop |sed -n 1p |awk '{print $1}'`
echo "pid=$pid"

CpuValue=`ps -p $pid -o pcpu |grep -v CPU`
echo "cpu=$CpuValue %"

MemUsage=`ps -o vsz -p $pid|grep -v VSZ`
(( MemUsage /= 1000 ))
echo "mem=$MemUsage M" 
