#!/bin/sh

if [ -e /tmp/PlasmaServers.exe.lock ]
  then
    kill `cat /tmp/PlasmaServers.exe.lock`
fi
