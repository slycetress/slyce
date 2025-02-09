
#!/bin/bash
echo "Installing Slyce AI dependencies..."
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
echo "Installation complete."

