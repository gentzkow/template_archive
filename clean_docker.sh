#!/bin/bash

TAG=$(date +%F)
MYHUBID=dataeditors
MYIMG=stata${VERSION}

docker image rm $MYHUBID/${MYIMG}:$TAG

docker container prune -f
