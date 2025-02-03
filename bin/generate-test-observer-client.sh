#!/bin/bash

uv tool run openapi-python-client generate \
    --url https://raw.githubusercontent.com/canonical/test_observer/refs/heads/ensure-up-to-date-openapi-schema/backend/schemata/openapi.json \
    --meta none \
    --output-path plugins/test_observer/lib \
    --overwrite
