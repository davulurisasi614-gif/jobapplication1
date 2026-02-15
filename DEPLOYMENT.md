# Alexa Job Portal - Deployment Checklist

## Pre-Deployment Checklist ✓

### Code Quality
- [x] Templates use professional design
- [x] CSS styling is complete and responsive
- [x] Views have error handling
- [x] Models are properly structured
- [x] URL routing is configured
- [x] Static files are properly configured

### Configuration Files
- [x] requirements.txt created with all dependencies
- [x] .gitignore file created
- [x] .env.example file created
- [x] README.md with documentation created
- [x] settings.py updated for production

### Security
- [x] DEBUG mode can be toggled via environment variable
- [x] SECRET_KEY moved to environment variable
- [x] ALLOWED_HOSTS configurable via environment variable
- [x] WhiteNoise added for static file serving
- [x] Security middleware added
- [x] CSRF protection enabled
- [x] Input validation in views
- [x] Authentication required for sensitive views

### Database
- [x] SQLite configured for development
- [x] Models have proper structure
- [x] Foreign keys properly defined
- [x] Status choices defined for Application model

### Static & Media Files
- [x] Static files directory created (static/css/)
- [x] CSS stylesheet complete and tested
- [x] Media files directory for resumes
- [x] WhiteNoise configured for static file serving

---

## Deployment Instructions

### 1. Local Development Testing
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your local settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### 2. Pre-Deployment Checklist

#### Environment Setup
- [ ] Create production .env file with:
  - [ ] Unique SECRET_KEY (`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
  - [ ] DEBUG=False
  - [ ] ALLOWED_HOSTS with your domain(s)
  - [ ] Database URL if using PostgreSQL

#### Database Setup (Production)
- [ ] Switch from SQLite to PostgreSQL:
  ```python
  # Set DATABASE_URL in .env
  DATABASES = {
      'default': dj_database_url.config(default='postgresql://user:password@host:port/dbname')
  }
  ```
- [ ] Run: `python manage.py migrate`

#### Static Files
- [ ] Run: `python manage.py collectstatic --noinput`
- [ ] Verify staticfiles/ directory is created
- [ ] Configure web server to serve from staticfiles/

#### Media Files
- [ ] Create media/ directory with proper permissions
- [ ] Consider using AWS S3 for media storage in production
- [ ] Set proper file permissions: `chmod -R 755 media/`

#### SSL/HTTPS
- [ ] Obtain SSL certificate
- [ ] Configure SECURE_SSL_REDIRECT = True
- [ ] Update .env with HTTPS domain

### 3. Choose Deployment Platform

#### Option A: Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY='your-secure-key'
heroku config:set DEBUG='False'
heroku config:set ALLOWED_HOSTS='your-domain.herokuapp.com'

# Add Procfile
echo "web: gunicorn jobapplication.wsgi" > Procfile

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

#### Option B: DigitalOcean / AWS / Linode
1. Provision a Linux server (Ubuntu 22.04 recommended)
2. Install Python 3.10+, PostgreSQL, Nginx
3. Setup virtual environment
4. Clone repository
5. Install dependencies
6. Configure Gunicorn:
   ```bash
   gunicorn jobapplication.wsgi:application --bind 0.0.0.0:8000
   ```
7. Setup systemd service for Gunicorn
8. Configure Nginx as reverse proxy
9. Setup SSL with Let's Encrypt

#### Option C: PythonAnywhere
1. Upload files via Web interface or Git
2. Create Python virtual environment
3. Install dependencies from requirements.txt
4. Create PostgreSQL database
5. Run migrations
6. Configure WSGI entry point
7. Add domain and enable HTTPS
8. Set environment variables in web app settings

#### Option D: Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "jobapplication.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 4. Post-Deployment Verification

- [ ] Test home page loads
- [ ] Test admin login
- [ ] Test job posting functionality
- [ ] Test job application
- [ ] Verify static files load (CSS, icons)
- [ ] Test resume upload to media folder
- [ ] Check database has correct data
- [ ] Test email notifications (if configured)
- [ ] Run security checks: `python manage.py check --deploy`

### 5. Monitoring & Maintenance

#### Regular Backups
```bash
# Backup database
pg_dump dbname > backup.sql

# Backup media files
tar -czf media_backup.tar.gz media/
```

#### Error Logging
Add error logging to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
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

#### Performance Monitoring
- Monitor server CPU and memory usage
- Check database query performance
- Setup uptime monitoring (UptimeRobot, Pingdom)
- Use Django Debug Toolbar in dev only

### 6. Security Best Practices After Deployment

- [x] DEBUG = False
- [x] SECRET_KEY is secret and unique
- [x] ALLOWED_HOSTS configured correctly
- [x] HTTPS/SSL enabled
- [x] Security headers configured
- [ ] Regular security updates applied
- [ ] Daily backups automated
- [ ] Error logs monitored
- [ ] Database access restricted
- [ ] Server firewall configured

### 7. Scaling Considerations

For future growth:
- Implement caching (Redis/Memcached)
- Setup database replication
- Use CDN for static files (CloudFront, Cloudflare)
- Implement load balancing
- Consider Celery for async tasks
- Setup email queue system

---

## Troubleshooting Guide

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput --clear
# Check nginx configuration points to staticfiles/
```

### Database Connection Error
- Verify DATABASE_URL in .env
- Check database credentials
- Ensure database server is running
- Check network connectivity

### Media Files Not Uploading
```bash
# Check permissions
chmod -R 755 media/
# Verify MEDIA_ROOT in settings.py
# Check disk space
df -h
```

### Gunicorn Not Starting
```bash
# Test configuration
gunicorn jobapplication.wsgi:application --bind 0.0.0.0:8000
# Check logs
journalctl -u gunicorn -n 50
```

### 502 Bad Gateway (Nginx)
- Check if Gunicorn process is running
- Verify Nginx upstream configuration
- Check Unix socket permissions
- Look at Nginx logs: `/var/log/nginx/error.log`

---

## Environment Variables Reference

```bash
# Required
SECRET_KEY=<your-unique-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Optional (Database)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Optional (Email)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# Optional (AWS S3)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

---

**Last Updated**: February 2026
**Status**: ✅ Ready for Deployment
