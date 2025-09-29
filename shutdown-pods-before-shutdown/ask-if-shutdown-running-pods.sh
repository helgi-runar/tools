#!/bin/bash

export RUNPOD_API_KEY="$(cat /home/helgi-runar/.runpod.key)"
running_pod_count=$( RUNPOD_API_KEY="$RUNPOD_API_KEY" /home/helgi-runar/development/runpod/list-running-pods.sh | wc -l)

if [[ -n "$running_pod_count" && "$running_pod_count" -gt 0 ]]; then
    if zenity --question --text="Do you want to shutdown all running pods (${running_pod_count} running)?" --title="Shutdown Confirmation"; then
        /home/helgi-runar/development/runpod/stop-all-pods.sh
    else
        echo "No pods will be shutdown."
    fi
else
    echo "Runpod count is: ${running_pod_count}"
fi
