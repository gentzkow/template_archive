#!/bin/bash
TAG=1.0
MYHUBID=jccisneros
MYIMG=template
STATALIC="/Applications/Stata/stata.lic"

DOCKER_BUILDKIT=1 docker build  . \
  --secret id=statalic,src="$STATALIC" \
  -t $MYHUBID/${MYIMG}:$TAG


docker run -it --rm \
  -v "${STATALIC}":/usr/local/stata/stata.lic \
  -v "$(pwd)":/home \
  $MYHUBID/${MYIMG}:${TAG}