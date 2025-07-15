#!/bin/bash
#
# Written by : Alejandro Villate
# Run this script from one directory above PE-portfolio/

set -eu

# Pull in latest changes
cd PE-portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate && pip install -r requirements.txt

# restart app service
systemctl daemon-reload
systemctl restart myportfolio