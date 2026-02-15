# Alexa - Professional Job Portal

A modern, professional job portal application built with Django that allows employers to post jobs and applicants to apply for positions.

## Features

- 🎯 Professional job listings display
- 📝 Post new job listings
- 📄 Resume upload and application management
- 👥 User authentication system
- 📱 Fully responsive design
- 🎨 Modern UI with Font Awesome icons
- 📊 Admin panel for managing jobs and applications

## Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Gunicorn
- **Icons**: Font Awesome 6.4.0

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd jobapplication
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
# Create a .env file in the root directory with:
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Usage

### For Job Seekers
1. Navigate to the home page
2. Browse available job listings
3. Click "Apply Now" on any job
4. Upload your resume
5. Submit your application

### For Employers
1. Log in to your admin account
2. Navigate to "Post a Job"
3. Fill in job details (title, location, description)
4. Click "Post Job"
5. Job will appear on the listings page

### Admin Panel
Access the admin panel at `/admin` with your superuser credentials to:
- View all posted jobs
- Manage job applications
- Update application status
- View user profiles

## Deployment

### For Production Deployment

1. **Update settings.py**
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS` with your domain
   - Store `SECRET_KEY` in environment variable
   - Use PostgreSQL instead of SQLite

2. **Set environment variables**
```bash
export SECRET_KEY='your-production-secret-key'
export DEBUG='False'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
```

3. **Run migrations on production**
```bash
python manage.py migrate
```

4. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

5. **Run with Gunicorn**
```bash
gunicorn jobapplication.wsgi:application --bind 0.0.0.0:8000
```

### Deployment Platforms

#### Heroku
```bash
heroku create your-app-name
heroku config:set SECRET_KEY='your-key'
heroku config:set DEBUG='False'
git push heroku main
heroku run python manage.py migrate
```

#### AWS/DigitalOcean
Use Gunicorn with Nginx reverse proxy and systemd service for process management.

#### PythonAnywhere
Upload files via web interface, configure WSGI entry point, and set environment variables in web app settings.

## Project Structure

```
jobapplication/
├── jobapplication/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── jobs/                    # Main app
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── apply_job.html
│   │   └── post_job.html
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── media/                   # User uploads
│   └── resumes/
├── static/                  # Static files
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page - list all jobs |
| GET | `/post/` | Post job form |
| POST | `/post/` | Submit new job |
| GET | `/apply/<job_id>/` | Apply for job form |
| POST | `/apply/<job_id>/` | Submit application |
| GET | `/admin/` | Admin panel |

## Configuration

### Database
- **Development**: SQLite (db.sqlite3)
- **Production**: PostgreSQL or MySQL

### Static Files
- CSS files: `static/css/`
- Media uploads: `media/resumes/`
- Collected static files: `staticfiles/`

### Settings to Update for Production
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jobportal_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Best Practices

1. ✅ Use environment variables for sensitive data
2. ✅ Set DEBUG = False in production
3. ✅ Update SECRET_KEY before deployment
4. ✅ Use HTTPS/SSL certificates
5. ✅ Keep Django updated
6. ✅ Use strong database passwords
7. ✅ Configure CORS properly
8. ✅ Validate user inputs
9. ✅ Use security headers (X-Frame-Options, etc.)
10. ✅ Regular security updates

## Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Permission Denied on Media Folder
```bash
chmod -R 755 media/
chmod -R 755 static/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please create an issue on GitHub.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

Created with ❤️ for job seekers and employers worldwide.

---

**Last Updated**: February 2026
**Version**: 1.0.0
