#!/bin/bash
#
# Written by : Alejandro Villate
# Run this script from the root directory (i.e. one directory above PE-portfolio/)

# Kill all existing tmux sessions
tmux kill-server

# Pull in latest changes
cd PE-portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate && pip install -r requirements.txt

# start a new detached tmux session to run app
tmux new-session -ds "flask-app"
tmux send-keys -t "flask-app" "source python3-virtualenv/bin/activate" C-m
tmux send-keys -t "flask-app" "flask run --host=0.0.0.0" C-m