#!/bin/bash
# Updates and cleans packages on Ubuntu/Debian systems
echo "🔄 Updating Linux packages..."
sudo apt update && sudo apt upgrade -y
echo "🧹 Cleaning up unused packages..."
sudo apt autoremove -y && sudo apt autoclean
echo "✅ System updated successfully!"
