#!/bin/bash

_ddi_completion() {
    local cur prev words cword

    cur="${COMP_WORDS[COMP_CWORD]}"  # Current word being completed
    prev="${COMP_WORDS[COMP_CWORD-1]}"  # Previous word

    # Handle 'm' subcommand for Docker image completion
    if [[ ${#COMP_WORDS[@]} -eq 2 ]]; then
        # Fetch Docker image names and filter by the current input
        local images
        images=$(docker images --format "{{.Repository}}" | grep -v "^<none>$" | grep "^$cur" 2>/dev/null)
        COMPREPLY=( $(compgen -W "$images" -- "$cur") )
        return
    fi
}

# Register the completion function for your script
complete -F _ddi_completion ddi
