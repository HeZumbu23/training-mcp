#!/usr/bin/env bash
# Installiert Abhaengigkeiten (falls noetig) und startet den dummy-mcp-server.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pip install -q -r "$SCRIPT_DIR/requirements.txt"
exec python3 "$SCRIPT_DIR/server.py" "$@"
