FROM debian:latest

# install requirements
RUN apt-get update && apt-get install -y \
    python3 \
    nodejs \
    curl \
    unzip \
    gcc \
    python3-venv \
    lm-sensors

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app

# setup virtual environment and initialize reflex
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt && \
    sudo lm-sensors && \
    reflex init

# Expose ports
EXPOSE 3000 8000

CMD ["reflex", "run"]