#!/bin/bash

export DISPLAY=:0.0
sudo xhost local:docker
sudo docker swarm leave --force
sudo docker-compose -f ../docker_compose_app.yml up --build
