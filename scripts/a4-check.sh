#!/bin/bash

# Path to pip requirement file
PIP_REQUIREMENTS_FILE="requirements/base.txt"

# Path to package.json file
PACKAGE_JSON_FILE="package.json"

# Package name
PACKAGE_NAME="adhocracy4"

# Read the hash from the pip requirements file
PIP_HASH=$(grep -E "$PACKAGE_NAME" "$PIP_REQUIREMENTS_FILE" | awk -F'@' '{print $2}' | awk -F'#' '{print $1}')

# Read the commit hash from the package.json file
PACKAGE_JSON_HASH=$(jq -r ".dependencies.\"$PACKAGE_NAME\"" "$PACKAGE_JSON_FILE" | awk -F'#' '{print $2}')

# Check if the hashes match
if [[ "$PIP_HASH" != "$PACKAGE_JSON_HASH" ]]; then
  echo "Hash for $PACKAGE_NAME does not match between pip and package.json."
  echo "PIP hash: $PIP_HASH"
  echo "package.json hash: $PACKAGE_JSON_HASH"
  exit 1
fi
