#!/usr/bin/env bash
# Wrapper to execute scripts/setup-mcps.sh from project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/scripts/setup-mcps.sh" "$@"
