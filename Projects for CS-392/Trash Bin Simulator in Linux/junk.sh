###############################################################################
# Authors: Rafael Sanchez & Sydney Cardy 
# Date: February 16th 2021
# Pledge: I pledge my honor that I have abided by the Stevens Honor System.
# Description: This simple shell script implements a recycle bin.
###############################################################################
#!/bin/bash

readonly recycle=~/.junk

if [ $# -eq 0 ]
then 
cat << ENDOFTEXT
Usage: $(basename "$0") [-hlp] [list of files]
    -h: Display help.
    -l: List junked files.
    -p: Purge all files.
    [list of files] with no other arguments to junk those files.
ENDOFTEXT
exit 1
fi

num_h=0
num_l=0
num_p=0

while getopts ":hlp" option; do
	case $option in
	h) (( num_h=num_h+1 ))
	   ;;
	l) (( num_l=num_l+1 ))
	   ;;
	p) (( num_p=num_p+1 ))
	   ;;
	?) cat << ENDOFTEXT
Error: Unknown option '-$OPTARG'.
Usage: $(basename "$0") [-hlp] [list of files]
    -h: Display help.
    -l: List junked files.
    -p: Purge all files.
    [list of files] with no other arguments to junk those files.
ENDOFTEXT
	   exit 1
	   ;;
	esac
done


declare -a filenames
shift "$(( OPTIND-1 ))"

index=0
for f in $@; do
	filenames[$index]="$f"
	(( ++index ))
done

(( valid_sum0=num_h+num_l+num_p ))
if [ $valid_sum0 -ge 1 ]
	then
	if [ ! -z $filenames ]
	then
cat << ENDOFTEXT
Error: Too many options enabled.
Usage: $(basename "$0") [-hlp] [list of files]
    -h: Display help.
    -l: List junked files.
    -p: Purge all files.
    [list of files] with no other arguments to junk those files.
ENDOFTEXT
	exit 1
	fi
fi


(( valid_sum=num_h+num_l+num_p ))
if [ $valid_sum -eq 1 ] 
	then
	if [ $num_h -eq 1 ]
	then
	cat << ENDOFTEXT
Usage: $(basename "$0") [-hlp] [list of files]
    -h: Display help.
    -l: List junked files.
    -p: Purge all files.
    [list of files] with no other arguments to junk those files.
ENDOFTEXT
	exit 0
	elif [ $num_l -eq 1 ]
	then

	ls -lAF $recycle
	
	exit 0
	else
	
	rm -rf $recycle/*
	rm -rf $recycle/.* 2> /dev/null
	exit 0
	fi
else
	if [ $valid_sum -gt 1 ]
	then
cat << ENDOFTEXT
Error: Too many options enabled.
Usage: $(basename "$0") [-hlp] [list of files]
    -h: Display help.
    -l: List junked files.
    -p: Purge all files.
    [list of files] with no other arguments to junk those files.
ENDOFTEXT
	exit 1
	fi
	
	if [ $valid_sum -eq 0 ]
	then
		if [ ! -z $filenames ]
		then
		
			mkdir -p $recycle
			
			for f in ${filenames[*]}; do
			
			if [ -e "$f" ]
			then
			mv $f $recycle
			else
			echo "Warning: '$f' not found."
			fi
			
			done
			exit 0
		
		fi
	fi
fi

