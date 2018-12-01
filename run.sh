#!/usr/bin/env bash

docker run -it --rm -v $(pwd):/opt/car-search -p 8888:8888 --name car-search car-search