#!/bin/bash

sudo apt update && sudo apt install -y python3-venv

if [ ! -d "myenv" ]; then
    python3 -m venv myenv
fi

source myenv/bin/activate
python3 install.py