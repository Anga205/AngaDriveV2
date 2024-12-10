# List of packages to search for
PACKAGES=("git" "python-virtualenv" "curl" "nodejs" "gcc" "python" "unzip" "lm-sensors")

# Loop through the packages and check if they are installed
for package in "${PACKAGES[@]}"; do
    if ! pacman -Q "$package" >/dev/null 2>&1; then
        echo "Package $package is not installed. Installing..."
        sudo pacman -S --noconfirm "$package"
    fi
done

if [ ! -d "venv" ]; then
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    reflex init
    deactivate
fi
source venv/bin/activate
reflex run --env prod