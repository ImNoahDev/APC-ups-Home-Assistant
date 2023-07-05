#!/bin/bash

# Define the session name and command to run
tmux new-session -d -s “apcpy” "pip install flask && python3 /boot/config/plugins/user.scripts/scripts/APC\ ups/apc.py"
echo "done"
