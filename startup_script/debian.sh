# List of packages to search for
PACKAGES=("git" "python3-venv" "curl" "nodejs" "gcc" "python3-dev" "unzip" "lm-sensors")

# Loop through the packages and check if they are installed
for package in "${PACKAGES[@]}"; do
    if ! dpkg -s "$package" >/dev/null 2>&1; then
        echo "Package $package is not installed. Installing..."
        sudo apt install -y "$package"
    fi
done


if [ ! -d "venv" ]; then
    python3 -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt
    reflex init
    deactivate
fi
source venv/bin/activate
reflex run --env prod