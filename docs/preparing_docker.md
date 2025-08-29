# Docker

> ***OBS:*** Vejledning i at lave Docker image - ikke relevant for brugere af programmet!

## Build docker image

docker build -t innotech-env:local .  

## Run local

docker run -it --name innotech-container -p 8888:8888 -p 8080:8080 -v ${PWD}:/home/jovyan/work innotech-env:local

docker rm innotech-container

## Push to Docker Hub

docker tag innotech-env:local anerv/innotech-env:latest

docker push anerv/innotech-env:latest

## Pull and run from Docker Hub

docker pull anerv/innotech-env:latest

docker run -it --name innotech-container -p 8888:8888 -p 8080:8080 -v ${PWD}:/home/jovyan/work innotech-env:latest

docker rm innotech-container