#!/bin/bash
echo "Installing dependencies for Slicenet..."
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
pip install flask requests

echo "Starting Slicenet AI..."
python3 server.py
