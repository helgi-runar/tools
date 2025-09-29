#!/bin/bash

PYTHON_VERSION=3.10.16
PYTHON_PATH="/home/runner/actions-runner/_work/_tool/Python/$PYTHON_VERSION/x64"

export PATH="$PYTHON_PATH/bin:$PATH"
export PYTHON_ROOT_DIR="$PYTHON_PATH"
export PYTHONHOME="$PYTHON_PATH"
export PKG_CONFIG_PATH="$PYTHON_PATH/lib/pkgconfig"
export LD_LIBRARY_PATH="$PYTHON_PATH/lib:$LD_LIBRARY_PATH"
