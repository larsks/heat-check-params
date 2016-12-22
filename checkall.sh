#!/bin/sh

if ! [ -d puppet ]; then
	echo "ERROR: This script must be run from the top level of" >&2
	echo "       the tripleo-heat-templates directory." >&2
	exit 1
fi

find puppet -name '*.yaml' \! -name '*.j2.yaml' -print |
xargs python check-params/check-params.py "$@"
