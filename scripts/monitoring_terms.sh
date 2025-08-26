#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

xfce4-terminal --command "bash $SCRIPT_DIR/run_dashboard.sh" --hide-borders --geometry 220x48+200+50 --hide-scrollbar

