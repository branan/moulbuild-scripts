#!/bin/sh

PID_FILE='/home/dirtsand/server/ds.pid'
 
if [ -e $PID_FILE ]
  then
    kill `cat $PID_FILE`
    rm $PID_FILE
fi
