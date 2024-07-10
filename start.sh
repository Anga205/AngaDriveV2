if [ ! -d "venv" ]; then
    python3 -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt
    reflex init
fi
reflex run