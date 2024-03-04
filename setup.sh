#!/usr/bin/env bash


if [ ! -d "venv" ]; then
	echo "Starting one-time setup"
	required_packages=("git" "python3-venv" "curl" "nodejs" "gcc" "python3-dev", "unzip")

	is_package_installed() {
		package=$1
		if dpkg -l | grep "^ii.* $package " > /dev/null; then
			return 1
		else
			echo "$package not found, installing automatically"
			return 0
		fi
	}

	for package in "${required_packages[@]}"; do
		if is_package_installed "$package"; then
			sudo apt install $package > /dev/null
		fi
	done


	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

	clear


	reflex init

else

	source venv/bin/activate

fi
reflex run