# Production Deployment Guide for mandad_backend

## Pre-Deployment Checklist

### 1. Environment Setup

- [ ] Set up PostgreSQL database on your VPS
- [ ] Create a database and user for the application
- [ ] Install Python 3.10+ on your VPS
- [ ] Install system dependencies: `sudo apt-get install python3-dev libpq-dev`

### 2. Environment Variables

Copy `.env.example` to `.env` and update with your production values:

```bash
cp .env.example .env
```

**Critical Variables:**

- `SECRET_KEY` - Generate a secure key (e.g., using `django-insecure-key-generator`)
- `DATABASE_URL` or individual `DB_*` variables pointing to your PostgreSQL instance
- `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` - Your SMTP credentials

### 3. Django Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Web Server Configuration

#### Option A: Using Gunicorn + Nginx (Recommended)

**Install Nginx:**

```bash
sudo apt-get install nginx
```

**Gunicorn Service File** (`/etc/systemd/system/gunicorn.service`):

```ini
[Unit]
Description=gunicorn daemon for mandad
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/mandad_backend
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/gunicorn.sock \
    mandad.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration** (`/etc/nginx/sites-available/mandad`):

```nginx
server {
    listen 80;
    server_name mandadmedical.com www.mandadmedical.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mandadmedical.com www.mandadmedical.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    # SSL hardening
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    client_max_body_size 100M;

    location /static/ {
        alias /path/to/mandad_backend/staticfiles/;
    }

    location /media/ {
        alias /path/to/mandad_backend/media/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/mandad /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt - Free)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d mandadmedical.com -d www.mandadmedical.com
```

Update the Nginx config with certificate paths from certbot.

### 6. Service Management

```bash
# Enable and start Gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# Check status
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### 7. Database Backups

Set up automated backups:

```bash
# Create backup script: /home/user/backup-db.sh
#!/bin/bash
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres mandad > "$BACKUP_DIR/mandad_$TIMESTAMP.sql"
# Keep only last 7 days
find "$BACKUP_DIR" -mtime +7 -delete
```

Add to crontab:

```bash
crontab -e
# Run daily at 2 AM
0 2 * * * /home/user/backup-db.sh
```

### 8. Monitoring & Logging

**Django Logging Configuration** (add to settings.py):

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/mandad/django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 9. Additional Security Hardening

- [ ] Change Django admin URL from `/admin/` to something obscure
- [ ] Enable 2FA/TOTP for admin accounts
- [ ] Set up firewall rules (ufw)
- [ ] Configure fail2ban for brute force protection
- [ ] Regular security updates: `sudo apt-get update && sudo apt-get upgrade`
- [ ] Monitor error logs regularly

### 10. Performance Optimization

- [ ] Enable database connection pooling (PgBouncer)
- [ ] Configure Redis for caching (optional)
- [ ] Enable gzip compression in Nginx
- [ ] Set up CDN for static files (CloudFront, Bunny CDN)

## Troubleshooting

**Gunicorn won't start:**

```bash
sudo journalctl -u gunicorn -n 50
```

**Permission denied errors:**

- Ensure www-data user has read access to the application directory
- Ensure www-data can write to media and log directories

**Database connection errors:**

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection string in `.env`
- Test connection: `psql -U postgres -d mandad -h localhost`

## Production Deployment Commands

```bash
# Full deployment procedure
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## Monitoring

Consider installing:

- **Sentry** for error tracking
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation
- **Uptime monitoring** (Uptimerobot, Pingdom)
