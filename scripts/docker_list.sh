#!/bin/bash

#This script will dump the contents of the docker images list
#on the current system into the specified text file in the
# following format:
#   <hash> <image_name> <version>
#   24f472f8d577 registry.access.redhat.com/rhscl/ruby-23-rhel7 latest 
#   ba9d222812cc registry.access.redhat.com/openshift3/node v3.9.40 
# Usage Example:
#  ./docker_list.sh image_list

sudo docker images | awk '{printf ("%s %s %s\n", $3,$1,$2)}' >> $1
