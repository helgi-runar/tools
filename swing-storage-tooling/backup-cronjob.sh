#!/bin/bash

cd $(realpath "$0" | sed 's|\(.*\)/.*|\1|')

python3 r2_to_s3_glacier_backup.py 6000
