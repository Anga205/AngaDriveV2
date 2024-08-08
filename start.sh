#!/bin/bash

if [[ -f /etc/debian_version ]]; then
    # Debian-based system
    . startup_script/debian.sh
elif [[ -f /etc/arch-release ]]; then
    # Arch-based system
    . startup_script/arch.sh
elif [[ -f /etc/redhat-release ]]; then
    # Red Hat-based system
    . startup_script/redhat.sh
else
    echo "Unsupported distribution"
fi