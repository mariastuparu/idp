#!/bin/bash

cd ..
sudo docker stack deploy -c docker-compose_monitor.yml fanficapp
sudo docker network create --driver overlay prom
sudo docker service create --name node --mode global --mount type=bind,source=/proc,target=/host/proc --mount type=bind,source=/sys,target=/host/sys --mount type=bind,source=/,target=/rootfs --network prom --publish 9100:9100 prom/node-exporter:v0.15.0 --path.procfs /host/proc --path.sysfs /host/sys --collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"
sudo docker service create --name cadvisor --network prom --mode global --mount type=bind,source=/,target=/rootfs --mount type=bind,source=/var/run,target=/var/run --mount type=bind,source=/sys,target=/sys --mount type=bind,source=/var/lib/docker,target=/var/lib/docker google/cadvisor:latest
sudo docker service create --replicas 1 --name metrics --network prom --mount type=bind,source=/home/maria/Documents/Facultate/Anul4II/IDP/Proiect/prometheus.yml,destination=/etc/prometheus/prometheus.yml --publish 9090:9090/tcp prom/prometheus