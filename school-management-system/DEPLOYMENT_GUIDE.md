# School Management System - Deployment Guide

## Overview
This guide covers deploying the School Management System to production using various platforms.

## Project Structure
```
school-management-system/
├── backend/          # Django REST API
│   ├── school_management/
│   ├── manage.py
│   └── requirements.txt
├── frontend/         # React Application
│   ├── src/
│   ├── package.json
│   └── public/
├── docker-compose.yml
├── Dockerfile.backend
└── Dockerfile.frontend
```

---

## Option 1: Deploy on Heroku (Recommended for Quick Start)

### Prerequisites
- Heroku CLI installed
- GitHub account with the repository

### Steps

1. **Login to Heroku:**
```bash
heroku login
```

2. **Create a new Heroku app:**
```bash
heroku create your-school-management-app
```

3. **Add PostgreSQL Database:**
```bash
heroku addons:create heroku-postgresql:standard-0 --app your-school-management-app
```

4. **Set environment variables:**
```bash
heroku config:set DEBUG=False --app your-school-management-app
heroku config:set SECRET_KEY=your-secure-random-key --app your-school-management-app
heroku config:set ALLOWED_HOSTS=your-school-management-app.herokuapp.com --app your-school-management-app
heroku config:set CORS_ALLOWED_ORIGINS=https://your-school-management-app.herokuapp.com --app your-school-management-app
```

5. **Deploy:**
```bash
git push heroku main
```

6. **Run migrations:**
```bash
heroku run python backend/manage.py migrate --app your-school-management-app
heroku run python backend/create_admin.py --app your-school-management-app
```

---

## Option 2: Deploy with Docker Compose Locally

### Steps

1. **Build images:**
```bash
docker-compose build
```

2. **Start services:**
```bash
docker-compose up -d
```

3. **Run migrations:**
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python create_admin.py
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

---

## Option 3: Deploy on Railway.app (Easiest)

### Steps

1. **Go to [railway.app](https://railway.app)**

2. **Connect GitHub repository**

3. **Create services:**
   - Backend service with Railway PostgreSQL
   - Frontend service

4. **Set environment variables:**
```
DEBUG=False
SECRET_KEY=your-secure-key
DATABASE_URL=your-railway-postgres-url
CORS_ALLOWED_ORIGINS=your-railway-domain.com
```

5. **Deploy!**

Railway automatically detects Procfile and deploys.

---

## Option 4: Deploy on PythonAnywhere

### Steps

1. **Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)**

2. **Upload code via Git:**
```bash
git clone your-repo-url
```

3. **Create virtual environment and install dependencies**

4. **Configure WSGI file** pointing to `backend/school_management/wsgi.py`

5. **Set up static files** in Web app settings

6. **Reload web app**

---

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate secure `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Update `CORS_ALLOWED_ORIGINS`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Collect static files
- [ ] Set up HTTPS
- [ ] Configure email backend
- [ ] Set up backups
- [ ] Monitor logs
- [ ] Set up error tracking (Sentry)

---

## Environment Variables Required

```
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=<your-domain>
DATABASE_URL=postgresql://user:password@host:5432/db_name
CORS_ALLOWED_ORIGINS=https://<your-domain>
ENVIRONMENT=production
```

---

## Database Migration (Production)

Run this command after deployment:

```bash
python backend/manage.py migrate
```

---

## Creating Admin User (Production)

```bash
python backend/manage.py createsuperuser
# or
python backend/create_admin.py
```

---

## Features Included

✅ User Authentication (Token-based)
✅ Student Management
✅ Class & Subject Management
✅ Attendance Tracking
✅ Fee Payment System
✅ Exam & Marks Management
✅ Results Publishing
✅ Transport Management
✅ Homework Assignment
✅ Notifications
✅ Library Management
✅ Complaint System
✅ Certificate Generation
✅ Advanced Filtering & Search
✅ Pagination
✅ API Documentation (Swagger)

---

## Support & Troubleshooting

### Static Files Not Loading
```bash
python backend/manage.py collectstatic --noinput
```

### Database Connection Issues
- Verify DATABASE_URL format
- Check PostgreSQL is running
- Test connection: `psql $DATABASE_URL`

### CORS Errors
- Check CORS_ALLOWED_ORIGINS matches frontend URL
- Verify browser dev tools Network tab

### Login Issues
- Ensure admin user created with `create_admin.py`
- Check token endpoint at `/api/auth/token/`

---

## Useful Commands

```bash
# Local development
npm start              # Frontend on port 3000
python manage.py runserver 0.0.0.0:8000  # Backend on port 8000

# Production
gunicorn school_management.wsgi:application

# Database
python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic

# Docker
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## Next Steps

1. Push code to GitHub
2. Choose deployment platform
3. Configure environment variables
4. Deploy application
5. Set up custom domain
6. Enable HTTPS
7. Monitor performance

For more details, visit the project repository.
