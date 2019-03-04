#!/bin/bash

echo "$@" > /data/111.txt
printenv > /data/222.txt
wget -q -O - "$@" "https://data.sfgov.org/api/views/yitu-d5am/rows.csv"
