#!/bin/bash
NAME=kick-api
docker build -t $NAME .
docker run -it --rm --name $NAME $NAME
