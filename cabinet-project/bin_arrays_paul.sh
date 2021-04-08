#!/bin/bash
#   ___  _________
#  / _ \/ __/ ___/  dencha@airmail.cc
# / // /\ \/ /__    github.com/ismashbuttons
#/____/___/\___/  
#
# bin arrays - use loops to add the filenames in bin lists to seperate arrays.
#

for i in {A..D}; do
  # inserted:
  declare -n array_i="array${i}"
  for j in $(cut -d ":" -f 1 bins_${i}.uniq.r1); do
    # modified: array${i}+=("${j}")
	array_i+=("${j}")
  done
  # inserted:
  unset -n array_i
done

echo "array A total: ${#arrayA[@]}"
echo "array B total: ${#arrayB[@]}"
echo "array C total: ${#arrayC[@]}"
echo "array D total: ${#arrayD[@]}"
