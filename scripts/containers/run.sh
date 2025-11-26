#!/bin/bash

export WORKING_DIRECTORY=$(pwd)
VERSION=${VERSION:-latest}

function clean-up () {
    if [ $# -eq 0 ]; then
        echo "No action specified, exiting clean-up."
        # echo "---Cleaning up Docker images and containers---"
        # docker system prune -a -f
        exit 0
    # given only image name
    elif [ $# -eq 1 ]; then
        local IMAGE_NAME=$1
        local IMAGE_ID=$(docker images -q $IMAGE_NAME 2> /dev/null)
        local container_id=$(get-container-id-by-image-name $IMAGE_NAME)
        if [ -z "$IMAGE_ID" ]; then
            echo "No image found for name: $IMAGE_NAME"
            exit 1
        fi
        if [ -z "$container_id" ]; then
            echo "No container found for image name: $IMAGE_NAME"
            exit 1
        fi
        echo "---Cleaning up Docker container ($container_id) and image ($IMAGE_NAME / $IMAGE_ID)---"
        docker stop $container_id
        docker rm -f $container_id
        docker rmi -f $IMAGE_ID
        exit 0

    # given both container id and image id
    elif [ $# -eq 2 ]; then
        echo "---Cleaning up Docker images and containers---"
        local container_id=$1
        docker rm -f $container_id
        local DOCKER_IMAGE_ID=$2
        docker rmi -f $DOCKER_IMAGE_ID
        exit 0
    else
        echo "Invalid number of arguments for clean-up"
        exit 1
    fi
}

function get-container-id-by-image-name () {
    docker ps -a --filter "ancestor=$1" -q | head -n 1
}

function get-logs-by-container-id () {
    docker logs -f $1
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
            echo "  - container ($container_id) already running with image ($image_id) $tag_name"
            echo ""
            echo "---Starting the existing Django Docker container ($container_id)---"
            docker start $container_id
            cd $WORKING_DIRECTORY || exit 1
            exit 0
        fi
        echo "  - Docker image ($image_id) $tag_name already exists."
        echo ""
        echo "---Running the Django Docker container---"
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
        echo "---Running the Django Docker container---"
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
            echo "---Running the Ubuntu 24 Docker container---"
            docker run -d -p 8080:80 $tag_name
        fi
    else
        echo "---Building Ubuntu 24 Docker image---"
        docker build -f "UBUNTU_24_DOCKFILE" -t $tag_name .
        if [ $? -ne 0 ]; then
            echo "  - Docker build failed."
            exit 1
        fi
        echo "---Running the Ubuntu 24 Docker container---"
        docker run -d -p 8080:80 $tag_name
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
        # django ${2:-$VERSION};;
        echo "WARNING: disabled for now -- need to run via docker-compose"
        echo "";;
    "ubuntu")
        ubuntu_24 ;;
    "enter")
        # pass all arguments to enter_container function except the first one
        enter_container "${@:2}" ;;
    "clean-up")
        clean-up "${@:2}" ;;
    "logs")
        get-logs-by-container-id "${@:2}" ;;
    *)
        echo "Unknown environment variable: $var_name" ;;
esac
