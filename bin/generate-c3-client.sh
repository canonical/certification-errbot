#!/bin/bash

MAX_RETRIES=3
RETRY_DELAY=5

run_with_retries() {
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        if uv tool run openapi-python-client generate \
            --url https://certification.canonical.com/api/v2/openapi \
            --meta none \
            --output-path plugins/certification/test_observer \
            --overwrite; then
            return 0
        else
            if [ $attempt -lt $MAX_RETRIES ]; then
                sleep $RETRY_DELAY
            fi
        fi
        
        ((attempt++))
    done
    
    return 1
}

run_with_retries