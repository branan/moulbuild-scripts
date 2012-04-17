#!/bin/bash

set -m

cd /home/dirtsand/server
#gdb -ex run --args ./bin/dirtsand /home/dirtsand/server/dirtsand.ini 2>&1 | tee serverlog
./bin/dirtsand /home/dirtsand/server/dirtsand.ini 2>&1 | tee serverlog
