#!/bin/sh

set -m

cd /home/dirtsand/server
./bin/dirtsand dirtsand.ini &
echo $! > ds.pid
fg
