#!/bin/bash

VERSION=17
TAG=$(date +%F)
MYHUBID=dataeditors
MYIMG=stata${VERSION}
STATALIC="/Applications/Stata/stata.lic"

DOCKER_BUILDKIT=1 docker build  . \
  --secret id=statalic,src="$STATALIC" \
  -t $MYHUBID/${MYIMG}:$TAG


docker run -it --rm \
  -v "${STATALIC}":/usr/local/stata/stata.lic \
  -v "$(pwd)":/home \
  $MYHUBID/${MYIMG}:${TAG}
