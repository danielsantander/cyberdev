#!/bin/bash


if [ $# -gt 0 ]; then
	OUTPUT_FILE="$1"
else
	#read -sp "Enter output filepath: " OUTPUT_FILE
	OUT_FILE="~/Desktop/test.jpg"
	echo "";
fi

#OUT_FILE = "~/Desktop/test.jpg"

#raspistill -vf -hf -t 0 --brightness 60 -o ~/Desktop/test.jpg
#raspistill -vf -hf -t 1 --brightness 60 -o ~/Desktop/test.jpg
raspistill -vf -hf -t 1 -br 65 -co 40 -sh 30 -sa 45 -o ~/Desktop/test.jpg
