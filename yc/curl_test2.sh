#!/bin/bash
log="curl2.log"
declare -i n=5
declare -a a=("192.168.0.1" "173.194.222.113" "87.250.250.242")

if [ -f $log ] 
	then
	/usr/bin/rm $log
fi

touch $log

for i in ${a[@]} 
do
	declare -i j=1
	while  ((j<=$n)) 
	do
			echo $i 
			if nc -w1 -z $i 80; 
				then date >> $log; echo "connected to $i tcp 80"  >> $log
				else date >> $log; echo "failed to connnect to $i tcp 80" >> $log
			fi
		let "j += 1"
	done
done
