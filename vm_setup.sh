#!/bin/bash
set -e

echo "1. Setting up autochecker user..."
if ! id -u autochecker > /dev/null 2>&1; then
    sudo adduser --disabled-password --gecos "" autochecker
fi

echo "2. Configuring SSH for autochecker..."
sudo mkdir -p /home/autochecker/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKiL0DDQZw7L0Uf1c9cNlREY7IS6ZkIbGVWNsClqGNCZ se-toolkit-autochecker" | sudo tee /home/autochecker/.ssh/authorized_keys
sudo chmod 700 /home/autochecker/.ssh
sudo chmod 600 /home/autochecker/.ssh/authorized_keys
sudo chown -R autochecker:autochecker /home/autochecker/.ssh

echo "3. Setting up environment variables..."
if [ ! -f .env.docker.secret ]; then
    cp .env.docker.example .env.docker.secret
fi

# Ensure CADDY_HOST_ADDRESS is 0.0.0.0
# Just in case it was changed
if grep -q "CADDY_HOST_ADDRESS=127.0.0.1" .env.docker.secret; then
    sed -i 's/CADDY_HOST_ADDRESS=127.0.0.1/CADDY_HOST_ADDRESS=0.0.0.0/g' .env.docker.secret
fi

echo "4. Starting Docker services..."
docker compose --env-file .env.docker.secret up -d --build

echo "✅ VM Setup Complete! You can now run the autochecker."
