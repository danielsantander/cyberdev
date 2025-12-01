
- [Install](#install)
- [Quick Tips](#quick-tips)
  - [Build Container](#build-container)
  - [Build with Docker Compose](#build-with-docker-compose)
  - [Enter Container](#enter-container)
- [Example Build](#example-build)
- [Prune and Delete](#prune-and-delete)

# Install

```shell
# Install via homebrew via MacOS
brew update
brew install docker

# Install on Linux
sudo apt install docker.io docker-compose
sudo systemctl start docker
```

# Quick Tips

## Build Container

`docker image build -t python:0.0.1 {Dockerfile_location}`

```shell
docker build --tag python-docker .
[+] Building 1.2s (14/14) FINISHED

# list containers
docker ps -a

# start container
docker start -i {container_id}

# run container
# - `d` Run container in background and print container ID
# - `p` Publish a container's port(s) to the host
docker run -d -p 8000:5000 python-docker

# test docker results
curl localhost:8000
Hello, World!
```

## Build with Docker Compose

```shell
# build within same directory of Dockerfile
docker-compose build --no-cache

# run
docker-compose up

# stop and remove
docker-compose down
```

## Enter Container

```shell
# depending on which shell to use, with the following options
# - `i` Interactive mode (Keep STDIN open even if not attached)
# - `t` Allocate a pseudo-TTY
docker exec -it {CONTAINER_ID} /bin/ash
docker exec -it {CONTAINER_ID} /bin/sh

# EXAMPLES:
# ----------
# execute crond help page
docker exec <container> crond --help
# list cronjobs
docker exec <container> cat /etc/crontabs/root
```

# Example Build

Use `mycron` to run Python scripts with a Docker container.

```shell
# build 'mycron' image
$ docker build -t mycron .

# run the image
$ docker run -ti mycron

# start image as interactive in an Alpine base container
# - `i` Interactive mode (Keep STDIN open even if not attached)
# - `t` Allocate a pseudo-TTY
docker exec -it {CONTAINER_ID} /bin/ash

# execute crond help page
docker exec {CONTAINER_ID} crond --help

# list of crontabs
docker exec {CONTAINER_ID} cat /etc/crontabs/root
```

# Prune and Delete

```shell
# remove all stopped containers, -f will not ask for confirmation (y/N)
docker container prune -f

# remove all docker images
docker images prune

# delete all containers including its volumes use, -f will force remove any running containers
docker rm -vf $(docker ps -aq)

# delete all the images
docker rmi -f $(docker images -aq)

# delete everything
# - all stopped containers
# - all networks not used by at least one container
# - all volumes not used by at least one container
# - all images without at least one container associated with it
# - all build cache
docker system prune -a --volumes
```
