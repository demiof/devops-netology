#!/bin/bash
log="curl3.log"
log_err="curl3_err.log"
declare -i n=5
declare -a a=("173.194.222.113" "192.168.0.1" "87.250.250.242")

if [ -f $log ] 
	then
	/usr/bin/rm $log
fi
if [ -f $log_err ]
	then
	/usr/bin/rm $log_err
fi

touch $log
touch $log_err

for i in ${a[@]} 
do
	declare -i j=1
	while  ((j<=$n)) 
	do
	
		nc -w1 -z $i 80; 

		if (($? != 0))
			then 
				echo $?
				date >> $log_err; echo "failed to connnect to $i tcp 80" >> $log_err
				exit
			else

			echo $i 
			date >> $log; echo "connected to $i tcp 80"  >> $log
	
		fi


		let "j += 1"
	done

done
