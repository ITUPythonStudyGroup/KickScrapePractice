#!/bin/bash
NAME=kick-scraper
docker build -t $NAME .
docker run -it --rm --name $NAME $NAME
