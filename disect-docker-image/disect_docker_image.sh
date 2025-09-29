#!/bin/bash

if [ -z "$1" ]; then
    echo "No image supplied, exiting."
    exit 1
fi

if [ ! -z "$2" ]; then
    docker history --format '{{.Size}}%{{.CreatedBy}}' --no-trunc "${1}" | sort -t '%' -rh  ${cut_cmd} | awk -F'%' '{ printf "%-10s %s\n", $1, $2 }'
else
    docker history --format '{{.Size}}%{{.CreatedBy}}' --no-trunc "${1}" | sort -t '%' -rh  ${cut_cmd} |  awk -F'%' '{ printf "%-10s %.80s\n", $1, $2 }'
fi
