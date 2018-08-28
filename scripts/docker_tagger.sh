#!/bin/bash

#This script will read input from a specified file
#and tag docker images based on the contents of the file
# File format:
#   <hash> <image_name> <version> 
#   24f472f8d577 registry.access.redhat.com/rhscl/ruby-23-rhel7 latest 
#   ba9d222812cc registry.access.redhat.com/openshift3/node v3.9.40 
# Usage Example:
#  ./docker_tagger.sh image_list

while IFS='' read -r line || [[ -n "$line" ]]; do
    DOCKER_HASH="`echo $line | awk '{ print $1}'`"
    DOCKER_IMAGE="`echo $line | awk '{ print $2 }'`"
    DOCKER_TAG="`echo $line | awk '{ print $3 }'`"

    sudo docker tag $DOCKER_HASH $DOCKER_IMAGE:$DOCKER_TAG
     
done < "$1"
