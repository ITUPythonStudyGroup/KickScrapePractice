#!/bin/bash
NAME=kick-api
docker run -p 80:80 -it --name $NAME $NAME
