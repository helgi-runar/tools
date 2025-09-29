#!/bin/bash

set -e
cp disect_docker_image.sh ~/.local/bin/ddi
sudo cp disect_completion.sh /usr/share/bash-completion/completions/ddi && sudo chmod 644 /usr/share/bash-completion/completions/ddi
source /usr/share/bash-completion/completions/ddi
echo "Build complete"
