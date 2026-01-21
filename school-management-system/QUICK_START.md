# School Management System - Quick Start Guide

## 🚀 Quick Deployment (Choose One)

### Option A: Railway.app (Easiest - 5 minutes)
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Connect PostgreSQL plugin
5. Set environment variables from `.env.production`
6. Deploy! Your app is live in ~5 minutes

**Cost:** Free tier available for testing

---

### Option B: Heroku (Traditional - 10 minutes)
```bash
# Install Heroku CLI
heroku login
heroku create your-school-app
heroku addons:create heroku-postgresql:standard-0
heroku config:set SECRET_KEY=your-secret-key DEBUG=False
git push heroku main
heroku run python backend/manage.py migrate
heroku run python backend/create_admin.py
```

**Cost:** Starting at $7/month

---

### Option C: Docker (Local/VPS - 15 minutes)
```bash
# Make sure Docker & Docker Compose are installed
docker-compose up -d

# Then run:
docker-compose exec backend python manage.py migrate
docker-compose exec backend python create_admin.py
```

Access at:
- Frontend: http://localhost:3000
- Admin: http://localhost:8000/admin

---

## 📋 Environment Variables

Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-very-secure-random-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:password@host/dbname
```

---

## ✨ Features Included

✅ **User Management**
- Role-based access (Admin, Teacher, Student, Parent)
- Token authentication
- Secure password reset

✅ **Student Management**
- Enrollment tracking
- Parent assignment
- Class assignment

✅ **Academic Management**
- Class & Subject management
- Attendance tracking
- Exam scheduling
- Mark entry & results
- Report cards

✅ **Financial Management**
- Fee structure setup
- Payment tracking
- Overdue payment alerts

✅ **Infrastructure**
- Transport routes
- Vehicle management
- Student assignments

✅ **Communication**
- Homework assignments
- Notifications
- Complaint system

✅ **Library**
- Book inventory
- Issue/return tracking

✅ **Certificates**
- Certificate generation
- Custom templates

✅ **API Documentation**
- Swagger/OpenAPI docs at `/api/docs/`
- Schema at `/api/schema/`

---

## 🔐 Security

- ✅ CORS protection
- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Password hashing (bcrypt)
- ✅ Rate limiting ready
- ✅ Token authentication

---

## 📊 Technology Stack

**Backend:**
- Django 4.2.7
- Django REST Framework
- PostgreSQL
- Gunicorn

**Frontend:**
- React 18
- Tailwind CSS
- React Router v6
- Axios

**DevOps:**
- Docker & Docker Compose
- GitHub Actions CI/CD
- Heroku/Railway deployment

---

## 🎯 Default Login

```
Username: admin
Password: admin123
```

⚠️ **Change this immediately in production!**

---

## 📖 Documentation

- [Full Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [API Documentation](http://localhost:8000/api/docs/) (local)
- [Architecture](./ARCHITECTURE.md)
- [Database Schema](./DATABASE.md)

---

## 🆘 Troubleshooting

### Frontend won't load
```bash
cd frontend && npm install && npm start
```

### Backend won't start
```bash
cd backend
source venv/bin/activate  # or .venv/Scripts/activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Database connection error
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check credentials

### CORS errors
- Update CORS_ALLOWED_ORIGINS in settings
- Restart backend server

---

## 🚢 Production Checklist

Before going live:
- [ ] Change admin password
- [ ] Set DEBUG=False
- [ ] Generate new SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure email settings
- [ ] Test all features
- [ ] Monitor logs

---

## 📞 Support

For issues or questions:
1. Check the docs
2. Review error logs
3. Open GitHub issue

---

## 📜 License

[Add your license here]

---

**Happy deploying! 🎉**
