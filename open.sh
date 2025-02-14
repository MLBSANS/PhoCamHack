#!/bin/bash

sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-venv python3-pip

if [ ! -d "myenv" ]; then
    python3 -m venv myenv
fi

source myenv/bin/activate
python3 install.py