#!/bin/sh

set -m

cd /home/branan/plasma/urulive/server
./bin/dirtsand dirtsand.ini &
echo $! > ds.pid
fg