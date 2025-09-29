#!/bin/bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

${SCRIPT_DIR}/ask-if-shutdown-running-pods.sh

shutdown now
