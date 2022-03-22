#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
source $SCRIPT_DIR/env.sh
if [ -f $SCRIPT_DIR/local_env.sh ]; then
    source $SCRIPT_DIR/local_env.sh
fi

flask run --host=0.0.0.0
