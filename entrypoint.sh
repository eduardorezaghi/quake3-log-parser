#!/bin/bash

if [[ "$1" == "pytest" ]]; then
    shift # remove pytest from the argument list
    pytest "$@"
else
    python src/main.py ./logs/"$@"
fi