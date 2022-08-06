Run Python scripts with a Docker container

Docker File -> creates -> Docker Image -> runs -> Docker Container

[source](https://docs.docker.com/language/python/build-images/#create-a-dockerfile-for-python)

# Build Docker Container
`docker image build -t python:0.0.1 <location_to_directory_holding_dockerfile>`

```shell
$ docker build --tag python-docker .
[+] Building 1.2s (14/14) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                         0.0s
 => => transferring dockerfile: 37B                                                                                                                                                                          0.0s
 => [internal] load .dockerignore                                                                                                                                                                            0.0s
 => => transferring context: 2B                                                                                                                                                                              0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                                                                                                   0.4s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:443aab4ca21183e069e7d8b2dc68006594f40bddf1b15bbd83f5137bd93e80e2                                                                              0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                                         0.0s
 => [internal] load .dockerignore                                                                                                                                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.9-alpine                                                                                                                                         0.3s
 => [1/5] FROM docker.io/library/python:3.9-alpine@sha256:89ea7c66e4acf3d466a7ba1a3c8cf20895e3d6e69c8f5b0b3ccd6ffaf38075bb                                                                                   0.0s
 => [internal] load build context                                                                                                                                                                            0.0s
 => => transferring context: 504B                                                                                                                                                                            0.0s
 => CACHED [2/5] WORKDIR /app                                                                                                                                                                                0.0s
 => CACHED [3/5] COPY ./src/requirements.txt requirements.txt                                                                                                                                                0.0s
 => CACHED [4/5] RUN pip3 install -r requirements.txt                                                                                                                                                        0.0s
 => [5/5] COPY . .                                                                                                                                                                                           0.0s
 => exporting to image                                                                                                                                                                                       0.0s
 => => exporting layers                                                                                                                                                                                      0.0s
 => => writing image sha256:4b5e67ca211b8b871785846da180f4fabe2762b2482d3ee8c54864165728a053                                                                                                                 0.0s
 => => naming to docker.io/library/python-docker                                                                                                                                                             0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them

$ docker run -d -p 8000:5000 python-docker
bc3ec8a8cf22cee61974fcff4b4d039d65ef9d78cd5f32519fda6228875c4263

$ docker ps -a
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS                       PORTS                                       NAMES
bc3ec8a8cf22   python-docker   "./entrypoint.sh"        3 seconds ago    Up 2 seconds                 0.0.0.0:8000->5000/tcp, :::8000->5000/tcp   exciting_noether
6195f5473e4b   2881589466f0    "./entrypoint.sh"        51 seconds ago   Created                      0.0.0.0:8000->5000/tcp, :::8000->5000/tcp   awesome_blackwell

$ curl localhost:8000
Hello, World!
```


# EXAMPLE 2
Build image with name 'mycron':
```shell
$ docker build -t mycron .
```

Run the image:
```shell
$ docker run -ti mycron
```

Start image as interactive:
**EXAMPLE** -- starting an interactive shell in an Alpine base container:
`$ docker exec -it <container name> /bin/ash`

where options:
-	`i` Interactive mode (Keep STDIN open even if not attached)
-	`t` Allocate a pseudo-TTY
> /bin/ash is Ash (Almquist Shell) provided by BusyBox


# Execute Commands within Container

Start container
```shell
$ docker start -i 9f60b8b225f4
```
Execute command line within the container:

Retrieve Alpine crond help docs:
```shell
$ docker exec 9f60b8b225f4 crond --help
BusyBox v1.34.1 (2022-04-04 10:19:27 UTC) multi-call binary.

Usage: crond [-fbS] [-l N] [-d N] [-L LOGFILE] [-c DIR]

	-f	Foreground
	-b	Background (default)
	-S	Log to syslog (default)
	-l N	Set log level. Most verbose 0, default 8
	-d N	Set log level, log to stderr
	-L FILE	Log to FILE
	-c DIR	Cron dir. Default:/var/spool/cron/crontabs
```

List of crontabs:
```shell
$ docker exec 9f60b8b225f4 cat /etc/crontabs/root
# do daily/weekly/monthly maintenance
# min	hour	day	month	weekday	command
*/15	*	*	*	*	run-parts /etc/periodic/15min
0	*	*	*	*	run-parts /etc/periodic/hourly
0	2	*	*	*	run-parts /etc/periodic/daily
0	3	*	*	6	run-parts /etc/periodic/weekly
0	5	1	*	*	run-parts /etc/periodic/monthly
```

Check whether scripts are likely to run, shows what should run but will not actually execute the scripts:
```shell
$ docker exec 9f60b8b225f4 run-parts --test /etc/periodic/15min
/etc/periodic/15min/my_script.sh
```