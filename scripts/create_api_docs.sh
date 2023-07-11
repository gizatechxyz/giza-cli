#!/bin/bash

set -xe

lazydocs \
    --output-path="./docs/reference/api" \
    --overview-file="README.md" \
    --src-base-url="https://github.com/gizatechxyz/giza-cli/blob/main/" \
    --no-watermark \
    --remove-package-prefix \
    giza
