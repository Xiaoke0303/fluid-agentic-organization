#!/bin/bash
# Tech Diagram Generator Wrapper for OpenClaw
source /root/.openclaw/workspace/venv/bin/activate
python /root/.openclaw/workspace/scripts/tech_diagram.py "$@"
