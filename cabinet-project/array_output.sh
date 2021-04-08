#!/bin/bash
#   ___  _________
#  / _ \/ __/ ___/  dennis.chaves@gmail.com
# / // /\ \/ /__    github.com/ismashbuttons
#/____/___/\___/  
#
# Hi Paul! I know the difference between [@] and [*]. I will attempt to explain.
# The difference between the two has to do with word-splitting. The differences are not apparent until you wrap the array in quotes.
# Really, the difference is only significant in situations where you have an array of strings.

# An array with three strings, two words per string:
Q3=("Lewis Hamilton" "Sebastian Vettel" "Max Verstappen")

# If we iterate through each index in the array, both outcomes still appear the same
# word-splitting occurs on whitespace.
for i in ${Q3[*]}; do
	echo $i
done

for i in ${Q3[@]}; do
	echo $i
done

# wrapping the array in quotes is when things change.
# when quoted, [*] doesn't do any word-splitting. The entire array is output in one long string:
for i in "${Q3[*]}"; do
	echo $i
done

# When quoted, [@] ignores the whitespace within the strings in the array. So the strings themselves remain intact:
for i in "${Q3[@]}"; do
	echo $i
done

# When you have an array of single-words, the syntax doesn't matter. Quoted or unquoted the output is the same.
# If you have an array of strings, and you want to preserve those strings use [@] in quotes.

# Now that I'm thinking about it, this is actually the same as when using * and @ for positional parameters.

echo $* # expands into the list of positional parameters, starting with 1.
echo $@ # expands into the list of positional parameters, starting with 1.
echo "$*" # expands as if all parameters were within one set of double quotes: "one two three"
echo "$@" # expands as if each parameter were in double quotes: "one" "two" "three"
