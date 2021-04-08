#!/bin/bash
#   ___  _________
#  / _ \/ __/ ___/	dennis.chaves@chesterton.com
# / // /\ \/ /__  	github.com/ismashbuttons
#/____/___/\___/  
#
# bin reporter - generate a list of NC programs that contain a mention of a bin in the mystery cabinet.
# list the filename, line number a bin is mentioned on, what bin is mentioned, and what part number is associated with that 5-digit filename.

# create arrays
# cut out filenames from list A and put them in an array
for file in $(cut -d ":" -f 1 bins_A.uniq.r1); do
  arrayA+=("$file")
done

# cut out filenames from list B and put them in an array
for file in $(cut -d ":" -f 1 bins_B.uniq.r1); do
  arrayB+=("$file")
done

# cut out filenames from list C and put them in an array
for file in $(cut -d ":" -f 1 bins_C.uniq.r1); do
  arrayC+=("$file")
done

# cut out filenames from list D and put them in an array
for file in $(cut -d ":" -f 1 bins_D.uniq.r1); do
  arrayD+=("$file")
done

if [[ -d reports ]]; then
  echo "reports dir exists"
else
  mkdir reports
fi

# process A-bins
echo "Processing A-bins..."
for (( i = 0; i < ${#arrayA[@]}; i = i+1 )); do
  # filename = i-th array index
  line=$(grep "${arrayA[$i]}" bins_A.uniq.r1 | cut -d ":" -f 2)
  bin=$(grep "${arrayA[$i]}" bins_A.uniq.r1 | grep -Eio 'A-?[[:digit:]]{2}')
  progN=$(echo "${arrayA[$i]}" | cut -c 1-5)
  partN=$(grep -E ",0?${progN}," CNC_program_log.csv | cut -d "," -f 3 )

  echo -e "filename: ${arrayA[$i]}\nline: ${line}\nbin: ${bin}\npart: ${partN}\n" >> reports/bin_A_report.txt
done

# process B-bins
echo "Processing B-bins..."
for (( i = 0; i < ${#arrayB[@]}; i = i+1 )); do
  # filename = i-th array index
  line=$(grep "${arrayB[$i]}" bins_B.uniq.r1 | cut -d ":" -f 2)
  bin=$(grep "${arrayB[$i]}" bins_B.uniq.r1 | grep -Eio 'B-?[[:digit:]]{2}')
  progN=$(echo "${arrayB[$i]}" | cut -c 1-5)
  partN=$(grep -E ",0?${progN}," CNC_program_log.csv | cut -d "," -f 3 )

  echo -e "filename: ${arrayB[$i]}\nline: ${line}\nbin: ${bin}\npart: ${partN}\n" >> reports/bin_B_report.txt
done

# process C-bins
echo "Processing C-bins..."
for (( i = 0; i < ${#arrayC[@]}; i = i+1 )); do
  # filename = i-th array index
  line=$(grep "${arrayC[$i]}" bins_C.uniq.r1 | cut -d ":" -f 2)
  bin=$(grep "${arrayC[$i]}" bins_C.uniq.r1 | grep -Eio 'C-?[[:digit:]]{2}')
  progN=$(echo "${arrayC[$i]}" | cut -c 1-5)
  partN=$(grep -E ",0?${progN}," CNC_program_log.csv | cut -d "," -f 3 )

  echo -e "filename: ${arrayC[$i]}\nline: ${line}\nbin: ${bin}\npart: ${partN}\n" >> reports/bin_C_report.txt
done

# process D-bins
echo "Processing D-bins..."
for (( i = 0; i < ${#arrayD[@]}; i = i+1 )); do
  # filename = i-th array index
  line=$(grep "${arrayD[$i]}" bins_D.uniq.r1 | cut -d ":" -f 2)
  bin=$(grep "${arrayD[$i]}" bins_D.uniq.r1 | grep -Eio 'D-?[[:digit:]]{2}')
  progN=$(echo "${arrayD[$i]}" | cut -c 1-5)
  partN=$(grep -E ",0?${progN}," CNC_program_log.csv | cut -d "," -f 3 )

  echo -e "filename: ${arrayD[$i]}\nline: ${line}\nbin: ${bin}\npart: ${partN}\n" >> reports/bin_D_report.txt
done