#!/bin/bash

while  ((1==1))
do
	curl http://localhost:8443
	if (( $? == 0 )) 
		then date >> curl.log
		else echo $?
	fi
done
