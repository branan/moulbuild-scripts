#!/bin/sh

PID_FILE='/home/branan/plasma/urulive/server/ds.pid'
 
if [ -e $PID_FILE ]
  then
    kill `cat $PID_FILE`
    rm $PID_FILE
fi