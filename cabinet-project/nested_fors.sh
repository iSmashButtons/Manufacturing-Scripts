#!/bin/bash
#   ___  _________
#  / _ \/ __/ ___/  dencha@airmail.cc
# / // /\ \/ /__    github.com/ismashbuttons
#/____/___/\___/  
#
# scriptName - description
#

for i in {1..4}; do
  echo "outer loop $i"
  for j in {A..D}; do
    echo -e "\tinner loop $j (outer loop $i)"
  done
done
