# Quick Start Guide

## School Management System - 5 Minute Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- pip and npm

## Option 1: Automated Setup (Linux/Mac)

```bash
cd school-management-system
chmod +x setup.sh
./setup.sh
```

## Option 2: Manual Setup

### Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd school-management-system/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py migrate

# Create superuser (skip with Enter if you want)
# python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Backend running at**: http://localhost:8000

### Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd school-management-system/frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Frontend running at**: http://localhost:3000

## First Login

### Default Credentials
After running migrations, create a superuser:

```bash
python manage.py createsuperuser
```

Example:
- Username: admin
- Email: admin@school.com
- Password: admin123 (or your choice)

### Access Points

1. **Frontend App**: http://localhost:3000
   - Login with your superuser credentials
   - Main interface for the application

2. **Admin Panel**: http://localhost:8000/admin
   - Django admin for advanced management
   - View and manage all database records

3. **API Documentation**: http://localhost:8000/api/docs/
   - Interactive Swagger UI
   - Test API endpoints
   - View request/response schemas

## Common Commands

### Backend Commands

```bash
# Run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Create new app
python manage.py startapp app_name

# Run server on different port
python manage.py runserver 0.0.0.0:8001

# Create fixture (backup data)
python manage.py dumpdata > backup.json

# Load fixture (restore data)
python manage.py loaddata backup.json

# Clear cache
python manage.py clear_cache

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell
```

### Frontend Commands

```bash
# Build for production
npm run build

# Run tests
npm test

# Eject configuration (one-way operation)
npm run eject

# Clear npm cache
npm cache clean --force
```

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'django'"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Error: "Address already in use"**
```bash
# Run on different port
python manage.py runserver 8001
```

**Database errors**
```bash
# Reset database (caution: deletes all data)
rm db.sqlite3
python manage.py migrate
```

### Frontend Issues

**Error: "Node modules not installed"**
```bash
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Kill process on port 3000 and restart
# Or run on different port:
PORT=3001 npm start
```

**CORS errors**
```bash
# Ensure backend is running at http://localhost:8000
# Check CORS_ALLOWED_ORIGINS in backend/school_management/settings.py
```

## Project Structure Reference

```
school-management-system/
├── backend/               # Django REST API
│   ├── school_management/
│   │   ├── core/         # Models and admin
│   │   ├── api/          # Views and serializers
│   │   ├── settings.py
│   │   └── urls.py
│   └── manage.py
├── frontend/             # React application
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   └── App.js
│   └── package.json
├── README.md             # Full documentation
├── DEVELOPMENT.md        # Developer guide
├── DATABASE.md           # Schema documentation
└── setup.sh             # Setup script
```

## Database Models Overview

The system includes 55+ models for:
- User Management (with roles)
- Student & Parent Management
- Attendance (Manual, Biometric)
- Fees & Payments
- Exams & Results
- Transport Management
- Homework & Assignments
- Library & Inventory
- Payroll & HR
- Complaints & Audit Logs

All using UUID primary keys for enhanced security.

## API Overview

**Main Endpoints**:
- `/api/users/` - User management
- `/api/students/` - Student records
- `/api/classes/` - Class management
- `/api/subjects/` - Subject management
- `/api/attendance/` - Attendance tracking
- `/api/exams/` - Examination system
- `/api/marks/` - Marks management
- `/api/results/` - Results & report cards
- `/api/fee-payments/` - Fee tracking
- `/api/transport-routes/` - Transport management
- `/api/homework/` - Assignment management
- `/api/library-books/` - Library catalog
- `/api/complaints/` - Grievance system

**Full API documentation**: http://localhost:8000/api/docs/

## Next Steps

1. **Explore the Admin Panel**
   ```
   http://localhost:8000/admin
   ```
   - Create academic years
   - Add schools and classes
   - Create users with different roles

2. **Create Sample Data**
   - Add subjects
   - Create classes
   - Register students
   - Assign teachers

3. **Test the Frontend**
   - Login with your credentials
   - View dashboard
   - Test different role access

4. **Customize**
   - Read [DEVELOPMENT.md](./DEVELOPMENT.md) for extending
   - Add new features
   - Modify models as needed

## Support & Resources

- **Documentation**: See [README.md](./README.md)
- **Developer Guide**: See [DEVELOPMENT.md](./DEVELOPMENT.md)
- **Database Schema**: See [DATABASE.md](./DATABASE.md)
- **API Docs**: http://localhost:8000/api/docs/

## Tips

💡 **Always keep both servers running**
- Backend on port 8000
- Frontend on port 3000

💡 **Use Django Admin for quick testing**
- Create test data
- Verify relationships
- Check database state

💡 **Check Network Tab**
- Browser DevTools → Network tab
- See API requests/responses
- Debug CORS or auth issues

💡 **Read the Logs**
- Backend logs in terminal 1
- Frontend logs in terminal 2
- Check browser console (F12)

---

**Happy Coding!** 🎓

For detailed documentation, refer to the markdown files in the project root.
