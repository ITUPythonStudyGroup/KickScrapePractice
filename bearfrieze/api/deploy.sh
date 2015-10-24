#!/bin/bash
NAME=registry.blackbeard.io/bearfrieze/kick-api
docker build -t $NAME .
docker login registry.blackbeard.io
docker push $NAME
