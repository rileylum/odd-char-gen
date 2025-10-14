# Deployment Guide for ODD Character Generator

## Prerequisites
- VPS with Ubuntu/Debian
- Python 3.12+
- uv installed
- Caddy web server installed
- Root/sudo access

## Deployment Steps

### 1. Transfer Files to VPS
```bash
# On your local machine
rsync -avz --exclude '.venv' --exclude '__pycache__' \
  /home/riley/dev/dnd/odd-char-gen/ user@your-vps:/var/www/odd-char-gen/
```

### 2. Install Dependencies on VPS
```bash
ssh user@your-vps
cd /var/www/odd-char-gen

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### 3. Set Up Systemd Service
```bash
# Copy service file
sudo cp odd-char-gen.service /etc/systemd/system/

# Edit the service file to match your paths and user
sudo nano /etc/systemd/system/odd-char-gen.service

# Set proper ownership (adjust user/group as needed)
sudo chown -R www-data:www-data /var/www/odd-char-gen

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable odd-char-gen
sudo systemctl start odd-char-gen

# Check status
sudo systemctl status odd-char-gen
```

### 4. Configure Caddy
```bash
# Edit Caddyfile and replace 'your-domain.com' with your actual domain
nano Caddyfile

# Copy to Caddy config location
sudo cp Caddyfile /etc/caddy/Caddyfile

# Reload Caddy
sudo systemctl reload caddy
```

### 5. Verify Deployment
Visit your domain in a browser. You should see the ODD Character Generator interface.

## Troubleshooting

### Check Application Logs
```bash
sudo journalctl -u odd-char-gen -f
```

### Check Caddy Logs
```bash
sudo journalctl -u caddy -f
```

### Restart Services
```bash
sudo systemctl restart odd-char-gen
sudo systemctl restart caddy
```

## Environment Variables
You can customize the service by editing `/etc/systemd/system/odd-char-gen.service`:

- `ENV=production` - Sets production mode (disables auto-reload, enables workers)
- `PORT=8000` - Port the application runs on

## Updating the Application
```bash
cd /var/www/odd-char-gen
git pull  # if using git
uv sync   # update dependencies if needed
sudo systemctl restart odd-char-gen
```
