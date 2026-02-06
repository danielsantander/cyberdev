#!/bin/bash

WORKING_DIRECTORY=$(pwd)
VERSION=${VERSION:-latest}

function clean-up () {
    if [ $# -eq 0 ]; then
        echo "  - ERROR: No action specified, exiting clean-up."
        # echo "---Cleaning up Docker images and containers---"
        # docker system prune -a -f
        exit 0
    # given only image name
    elif [ $# -eq 1 ]; then
        local image_name=$1
        local image_id=$(docker images -q $image_name 2> /dev/null)
        local container_id=$(get-container-id-by-image-name $image_name)
        if [ -z "$image_id" ]; then
            echo "  - ERROR: No image found for name: $image_name"
            exit 1
        fi
        if [ -z "$container_id" ]; then
            echo "No container found for image name: $image_name"
            exit 1
        fi
        echo "---CLEANING UP DOCKER CONTAINER ($container_id) AND IMAGE ($image_name / $image_id)---"
        docker stop $container_id
        docker rm -f $container_id
        docker rmi -f $image_id
        exit 0

    # given both container id and image id
    elif [ $# -eq 2 ]; then
        local container_id=$1
        local image_id=$2
        echo "---CLEANING UP DOCKER CONTAINER ($container_id) AND IMAGE ($image_id)---"
        docker rm -f $container_id
        docker rmi -f $image_id
        exit 0
    else
        echo "  - ERROR: Invalid number of arguments for clean-up"
        exit 1
    fi
}

function get-container-id-by-image-name () {
    docker ps -a --filter "ancestor=$1" -q | head -n 1
}

function get-logs-by-container-id () {
    docker logs -f $1
}

function django-docker-compose () {
    container_name="djs-django"
    tmp_working_directory="$(dirname "$0")/dockerfiles/django/"
    cd "$tmp_working_directory" || exit 1
    container_id=$(docker ps -aqf "name=$container_name")
    if [ -n "$container_id" ]; then
        echo "  - WARNING: container $container_name already exists ($container_id)"
        echo ""
        echo "---STARTING THE EXISTING DJANGO DOCKER CONTAINER ($container_id)---"
        sudo docker-compose start
        cd $WORKING_DIRECTORY || exit 1
        return 0
    else
        echo -n "---BUILDING AND RUNNING THE DJANGO DOCKER CONTAINER---"
        sudo docker-compose up --build -d
        if [ $? -ne 0 ]; then
            echo "  - ERROR: DOCKER BUILD FAILED."
        else
            cd $WORKING_DIRECTORY || exit 1
            return 0
        fi

    fi
    cd $WORKING_DIRECTORY || exit 1
    return 1
}

function django () {
    # TODO: implement docker-compose for easier management
    app_name="djs-django"
    version=${1:-$VERSION}
    tag_name="${app_name}:${version}"
    tmp_working_directory="$(dirname "$0")/dockerfiles/django/"
    tmp_dockerfile="Dockerfile"
    cd "$tmp_working_directory" || exit 1
    image_id=$(docker images -q $tag_name 2> /dev/null)
    if [ -n "$image_id" ]; then
        container_id=$(docker ps -a --filter "ancestor=$image_id" --format "{{.ID}}")
        if [ -n "$container_id" ]; then
            echo "  - WARNING: container ($container_id) already running with image ($image_id) $tag_name"
            echo ""
            echo "---STARTING THE EXISTING DJANGO DOCKER CONTAINER ($container_id)---"
            docker start $container_id
            cd $WORKING_DIRECTORY || exit 1
            exit 0
        fi
        echo "  - Docker image ($image_id) $tag_name already exists."
        echo ""
        echo "---RUNNING THE DJANGO DOCKER CONTAINER---"
        # detached mode (-d) to get terminal back after starting container
        docker run -d -p 8000:8000 $tag_name
    else
        echo "---Building Django Docker image---"
        docker build -f $tmp_dockerfile -t $tag_name . --no-cache
        if [ $? -ne 0 ]; then
            echo "  - Docker build failed."
            cd $WORKING_DIRECTORY
            exit 1
        fi
        echo "---RUNNING THE DJANGO DOCKER CONTAINER---"
        # detached mode (-d) to get terminal back after starting container
        docker run -d -p 8000:8000 $tag_name
    fi

    cd $WORKING_DIRECTORY || exit 1
    exit 0
}

function ubuntu_24 () {
    tag_name="djs:ubuntu24"
    tmp_working_dir="$(dirname "$0")/dockerfiles/ubuntu24/"
    tmp_dockerfile="UBUNTU_24_DOCKFILE"
    cd "$tmp_working_dir" || exit 1

    # get image id by name
    image_id=$(docker images -q $tag_name 2> /dev/null)
    if [ -n "$image_id" ]; then
        # check if any container is running with this image
        local container_ids=$(docker ps -a --filter "ancestor=$image_id" --format "{{.ID}}")
        if [ -n "$container_ids" ]; then
            echo "  - container ($container_ids) already running with image ($image_id) $tag_name"
            echo ""
            echo "---Starting the existing Ubuntu 24 Docker container ($container_ids)---"
            docker start $container_ids
            exit 0
        else
            echo "  - no running container found with image id $image_id"
            echo ""
            echo "---Running the Ubuntu 24 Docker container with volume mounting---"
            docker run -d -p 8080:80 -v "./index.html:/var/www/html/index.html" $tag_name
        fi
    else
        echo "---Building Ubuntu 24 Docker image---"
        docker build -f "UBUNTU_24_DOCKFILE" -t $tag_name .
        if [ $? -ne 0 ]; then
            echo "  - Docker build failed."
            exit 1
        fi
        echo "---Running the Ubuntu 24 Docker container with volume mounting---"
        docker run -d -p 8080:80 -v "./index.html:/var/www/html/index.html" $tag_name
    fi

    cd $WORKING_DIRECTORY || exit 1
    exit 0
}

function enter_container () {
    local container_id=$1
    if [ -z "$container_id" ]; then
        echo "No container ID provided. Usage: ./run.sh enter [container_id]"
        exit 1
    fi
    docker exec -it $container_id /bin/bash
}


if [ $# -eq 0 ]; then
    echo "No action specified. Usage: ./run.sh [django|ubuntu|enter|clean-up|logs] [args...]"
    exit 1
fi
case $1 in
    "django")
        # echo "WARNING: disabled for now -- need to run via docker-compose"
        # django ${2:-$VERSION};;
        django-docker-compose ${2:-$VERSION};;
    "ubuntu")
        ubuntu_24 ;;
    "enter")
        if [ $# -lt 2 ]; then
            echo "No container ID provided. Usage: ./run.sh enter [container_id]"
            exit 1
        fi
        # pass all arguments to enter_container function except the first one
        enter_container "${@:2}" ;;
    "clean-up")
        if [ $# -lt 2 ]; then
            echo "No arguments provided for clean-up. Usage: ./run.sh clean-up [image_name] or ./run.sh clean-up [container_id] [image_id]"
            exit 1
        fi
        clean-up "${@:2}" ;;
    "logs")
        if [ $# -lt 2 ]; then
            echo "No container ID provided. Usage: ./run.sh logs [container_id]"
            exit 1
        fi
        get-logs-by-container-id "${@:2}" ;;
    *)
        echo "Unknown environment variable: $var_name" ;;
esac
