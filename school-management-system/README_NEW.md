# School Management System 🎓

A comprehensive, full-stack web application for managing school operations including students, classes, attendance, fees, exams, and more.

[![CI/CD](https://github.com/anurag9931043461/mtcs/workflows/CI%2FCD/badge.svg)](https://github.com/anurag9931043461/mtcs/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Features

### 👥 User Management
- Role-based access control (Admin, Teacher, Student, Parent)
- Secure token-based authentication
- User profile management
- Password reset functionality

### 📚 Academic Management
- Student enrollment and tracking
- Class and subject management
- Academic year configuration
- Parent-student assignment

### 📋 Attendance
- Daily attendance marking
- Biometric attendance support
- Attendance reports
- Automated alerts for absenteeism

### 📊 Examination System
- Exam scheduling
- Mark entry and management
- Result publishing
- Report card generation
- Certificate generation

### 💰 Financial Management
- Fee structure setup
- Payment tracking
- Overdue payment alerts
- Payment history
- Financial reports

### 🚌 Transport Management
- Route management
- Vehicle inventory
- Driver management
- Student-route assignment

### 📝 Academic Features
- Homework assignments
- Class diaries
- Library management
- Complaint system
- Notifications

### 🔒 Security Features
- CORS protection
- CSRF protection
- SQL injection prevention
- XSS protection
- Password hashing

---

## 🏗️ Architecture

```
School Management System
├── Backend (Django REST API)
│   ├── Authentication & Authorization
│   ├── Business Logic
│   ├── Database Models
│   └── API Endpoints
├── Frontend (React SPA)
│   ├── User Interface
│   ├── State Management
│   ├── API Client
│   └── Responsive Design
└── Database (PostgreSQL)
    └── Relational Data Storage
```

---

## 🚀 Quick Start

### Option 1: Local Development

**Prerequisites:**
- Python 3.12+
- Node.js 18+
- PostgreSQL 12+

**Setup:**

```bash
# Clone repository
git clone https://github.com/anurag9931043461/mtcs.git
cd school-management-system

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python create_admin.py

# Start backend (in backend directory)
python manage.py runserver 0.0.0.0:8000

# Frontend setup (in new terminal, from frontend directory)
cd ../frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Panel: http://localhost:8000/admin
- API Docs: http://localhost:8000/api/docs/

### Option 2: Docker

```bash
docker-compose up -d
```

Access at http://localhost:3000

### Option 3: Deploy Online

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for:
- Heroku deployment
- Railway.app deployment
- AWS/DigitalOcean deployment
- VPS setup

---

## 📖 Documentation

- [Quick Start Guide](./QUICK_START.md) - Get running in 5 minutes
- [Deployment Guide](./DEPLOYMENT_GUIDE.md) - Production deployment
- [API Guide](./API_GUIDE.md) - API endpoints and usage
- [Architecture](./ARCHITECTURE.md) - System design and structure
- [Database Schema](./DATABASE.md) - Data models
- [Development Guide](./DEVELOPMENT.md) - Contributing and development

---

## 🔐 Default Credentials

```
Username: admin
Password: admin123
```

⚠️ **Change immediately in production!**

---

## 📦 Tech Stack

### Backend
- **Framework:** Django 4.2.7
- **API:** Django REST Framework 3.14
- **Database:** PostgreSQL
- **Authentication:** Token Authentication
- **Documentation:** drf-spectacular

### Frontend
- **Library:** React 18.2
- **Router:** React Router v6
- **Styling:** Tailwind CSS 3.3
- **HTTP Client:** Axios
- **Icons:** Lucide React

### DevOps
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Heroku/Railway

---

## 📊 Database Models

### Core
- User (Custom)
- School
- Academic Year
- Class
- Subject
- Student
- Parent
- Staff

### Academic
- Attendance Record
- Exam
- Mark
- Result
- Certificate

### Financial
- Fee Structure
- Fee Payment

### Infrastructure
- Transport Route
- Vehicle

### Communication
- Homework
- Notification
- Complaint
- Class Diary

### Library
- Library Book

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/token/          - Get authentication token
GET    /api/users/profile/       - Get current user profile
```

### Resources
```
GET    /api/students/            - List students
POST   /api/students/            - Create student
GET    /api/students/{id}/       - Get student detail
PUT    /api/students/{id}/       - Update student
DELETE /api/students/{id}/       - Delete student

GET    /api/attendance/          - List attendance
POST   /api/attendance/          - Mark attendance

GET    /api/exams/               - List exams
GET    /api/marks/               - List marks
POST   /api/marks/               - Create mark

... and more endpoints
```

**See [API_GUIDE.md](./API_GUIDE.md) for complete API documentation.**

---

## 🔄 Workflow

### User Registration Flow
1. Admin creates user account
2. User logs in with credentials
3. Token is generated and stored locally
4. Token included in all API requests
5. Automatic token refresh

### Student Enrollment
1. Admin/Teacher adds new student
2. System auto-generates roll number
3. Parent account can be linked
4. Classes assigned
5. Enrollment verified

### Attendance Marking
1. Teacher opens attendance module
2. Selects class and date
3. Marks attendance status
4. System records with timestamp
5. Reports auto-generated

### Exam & Results
1. Admin creates exam schedule
2. Teacher enters marks
3. System calculates grades
4. Results published to students
5. Reports generated

---

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📋 Roadmap

- [ ] Mobile app (React Native)
- [ ] Video conferencing integration
- [ ] Advanced analytics dashboard
- [ ] AI-powered attendance analysis
- [ ] Multi-language support
- [ ] SMS/Email notifications
- [ ] Biometric attendance
- [ ] Online exam system

---

## 🐛 Bug Reports & Features

Found a bug? Have a feature idea?
[Open an issue](https://github.com/anurag9931043461/mtcs/issues)

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **Anurag Singh** - *Initial work*

---

## 🙏 Acknowledgments

- Django & Django REST Framework teams
- React community
- All contributors and users

---

## 📞 Support

Need help?
- 📖 Check [Documentation](./DEVELOPMENT.md)
- 💬 Open [GitHub Issue](https://github.com/anurag9931043461/mtcs/issues)
- 📧 Email support

---

## 🎯 Status

✅ **Active Development**

- Last Updated: 2026-01-21
- Version: 1.0.0
- Status: Production Ready

---

**Built with ❤️ for educational institutions**
