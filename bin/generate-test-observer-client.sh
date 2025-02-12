#!/bin/bash

uv tool run openapi-python-client generate \
    --url https://raw.githubusercontent.com/canonical/test_observer/refs/heads/main/backend/schemata/openapi.json \
    --meta none \
    --output-path plugins/certification/test_observer \
    --overwrite
