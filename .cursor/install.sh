#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for the Knock skills repository.
set -euo pipefail

cd "$(dirname "$0")/.."

python3 .cursor/validate-skills.py

# The skills document the Knock CLI. Install it onto the default PATH
# without changing shell profiles. A second run refreshes the same prefix.
mkdir -p "${HOME}/.local"
npm install -g --prefix "${HOME}/.local" @knocklabs/cli
sudo -n ln -sfn "${HOME}/.local/bin/knock" /usr/local/bin/knock
