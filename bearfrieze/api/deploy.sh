#!/bin/bash
NAME=kick-api
docker build -t $NAME .
docker stop $NAME
docker rm $NAME
docker run -p 80:80 -d --restart=always --name $NAME $NAME
