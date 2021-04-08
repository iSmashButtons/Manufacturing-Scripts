#!/bin/bash
#   ___  _________
#  / _ \/ __/ ___/	dennis.chaves@chesterton.com
# / // /\ \/ /__  	github.com/ismashbuttons
#/____/___/\___/  
#
# bin-reporter prototype: produce a report for one group of bins

# cut out filenames from list C and put them in an array
for file in $(cut -d ":" -f 1 bins_C.uniq.r1); do
  arrayC+=("$file")
done

# process C-bins
echo "Processing C-bins..."
for (( i = 0; i < ${#arrayC[@]}; i = i+1 )); do
  # filename = i-th array index
  line=$(grep "${arrayC[$i]}" bins_C.uniq.r1 | cut -d ":" -f 2)
  bin=$(grep "${arrayC[$i]}" bins_C.uniq.r1 | grep -Eio 'C-?[[:digit:]]{2}')
  progN=$(echo "${arrayC[$i]}" | cut -c 1-5)
  partN=$(grep -E ",0?${progN}," CNC_program_log.csv | cut -d "," -f 3 )

  echo -e "filename: ${arrayC[$i]}\nline: ${line}\nbin: ${bin}\npart: ${partN}\n" >> reports/one-bin_report.txt
done
