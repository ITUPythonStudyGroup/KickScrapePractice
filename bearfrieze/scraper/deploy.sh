#!/bin/bash
NAME=registry.blackbeard.io/bearfrieze/kick-scraper
docker build -t $NAME .
docker login registry.blackbeard.io
docker push $NAME
