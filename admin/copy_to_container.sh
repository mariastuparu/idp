#!/bin/bash

CONT_ID=$(sudo docker ps -aqf "name=proiect_client")
sudo docker cp $CONT_ID:./poze/genresPictures/$1 ./genres/$1