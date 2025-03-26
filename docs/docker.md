- [Build Container](#build-container)
- [Enter Container Interactively](#enter-container-interactively)
- [Example Build](#example-build)

# Build Container

`docker image build -t python:0.0.1 <location_to_directory_holding_dockerfile>`

```shell
docker build --tag python-docker .
[+] Building 1.2s (14/14) FINISHED

# list containers
docker ps -a

# start container
docker start -i <container_id>

# run container
# - `d` Run container in background and print container ID
# - `p` Publish a container's port(s) to the host
docker run -d -p 8000:5000 python-docker

# test docker results
curl localhost:8000
Hello, World!
```

# Enter Container Interactively

Usage: `docker exec -it <container name> command`

- `i` Interactive mode (Keep STDIN open even if not attached)
- `t` Allocate a pseudo-TTY

```shell
docker exec -it <container> /bin/ash
docker exec -it <container> /bin/sh

# execute crond help page
docker exec <container> crond --help

# list cronjobs
docker exec <container> cat /etc/crontabs/root
```

# Example Build

Use mycron to run Python scripts with a Docker container.

```shell
# build 'mycron' image
$ docker build -t mycron .

# run the image
$ docker run -ti mycron

# start image as interactive in an Alpine base container
# - `i` Interactive mode (Keep STDIN open even if not attached)
# - `t` Allocate a pseudo-TTY
docker exec -it <container name> /bin/ash

# execute crond help page
docker exec <container_id> crond --help

# list of crontabs
docker exec <container_id> cat /etc/crontabs/root
```
