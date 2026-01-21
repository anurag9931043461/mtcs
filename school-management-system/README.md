# School Management System

A comprehensive, full-featured School Management System built with Django REST Framework and React.

## Features

- **User Management**: Role-based access control (Super Admin, Admin, Teacher, Student, Parent, Accountant, Transport Manager)
- **Student Management**: Complete student profiles with parent relationships
- **Attendance Management**: Manual, biometric, and AI face detection support
- **Fees Management**: Fee structures, discounts, payments, and invoice generation
- **Examination System**: Exam scheduling, marks entry, auto-result calculation, report cards
- **Transport Management**: Routes, vehicles, driver management, GPS tracking ready
- **Homework & Diary**: Assignment tracking and class diary
- **Library Management**: Book inventory and transaction tracking
- **Payroll System**: Salary management for staff
- **Communication**: Notifications, SMS alerts, email integration ready
- **Complaints & Grievances**: Issue tracking and resolution
- **Audit Logging**: Complete audit trails for compliance
- **Certificates**: Automated certificate generation

## Technology Stack

- **Backend**: Python Django + Django REST Framework
- **Frontend**: React 18 with Tailwind CSS
- **Database**: SQLite (expandable to PostgreSQL/MySQL)
- **Primary Keys**: UUID (globally unique identifiers)

## Project Structure

```
school-management-system/
├── backend/
│   ├── school_management/
│   │   ├── core/              # Core app with all models
│   │   ├── api/               # API endpoints and serializers
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py            # WSGI config
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   └── db.sqlite3             # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API service calls
│   │   ├── context/           # React context (Auth)
│   │   ├── utils/             # Utility functions
│   │   ├── App.js             # Main app component
│   │   ├── index.js           # React entry point
│   │   └── index.css          # Global styles
│   ├── package.json           # Node dependencies
│   └── tailwind.config.js     # Tailwind configuration
├── README.md                  # This file
└── .env.example               # Environment variables template
```

## Database Models

### Core Models
- **User**: Custom user model with UUID and roles
- **AcademicYear**: School academic year configuration
- **School**: School information
- **Class**: Class/grade configuration
- **Subject**: Subject configuration
- **Student**: Student profiles with parent relationships
- **Parent**: Parent/guardian profiles
- **Staff**: Teacher and staff profiles

### Academic Models
- **AttendanceRecord**: Student daily attendance
- **BiometricAttendance**: Biometric attendance records
- **Exam**: Exam configuration and scheduling
- **ExamSchedule**: Subject-wise exam schedules
- **Mark**: Individual student exam marks
- **Grade**: Grade configuration
- **Result**: Exam results with auto-calculation
- **ReportCard**: Student report cards

### Finance Models
- **FeeStructure**: Fee structure configuration
- **FeeDiscount**: Fee discounts and waivers
- **FeePayment**: Fee payment tracking
- **Invoice**: Student invoices
- **Salary**: Staff salary management

### Other Models
- **TransportRoute**: Transport routes and stops
- **Vehicle**: Bus/vehicle information
- **Driver**: Driver details
- **StudentTransport**: Student-transport assignments
- **Homework**: Assignment management
- **LibraryBook**: Library inventory
- **InventoryItem**: General inventory tracking
- **Complaint**: Complaint and grievance system
- **Notification**: System notifications and alerts
- **AuditLog**: Security and compliance audit trails
- **Certificate**: Certificate generation and tracking

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd school-management-system/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd school-management-system/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env.local
   # Set REACT_APP_API_URL=http://localhost:8000/api
   ```

4. **Start development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/profile/` - Get current user profile

### Students
- `GET /api/students/` - List students
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get student details
- `GET /api/students/{id}/attendance/` - Get student attendance
- `GET /api/students/{id}/fee_details/` - Get student fee details

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Mark attendance
- `POST /api/attendance/bulk_mark/` - Bulk mark attendance

### Fees
- `GET /api/fee-structures/` - List fee structures
- `GET /api/fee-payments/` - List fee payments
- `GET /api/fee-payments/overdue/` - Get overdue payments
- `POST /api/fee-payments/` - Create fee payment

### Exams & Marks
- `GET /api/exams/` - List exams
- `POST /api/exams/{id}/publish_results/` - Publish exam results
- `GET /api/marks/` - List marks
- `POST /api/marks/bulk_upload/` - Bulk upload marks
- `GET /api/results/` - List results

### And many more... (see [API Documentation](./API_DOCS.md))

## Admin Panel

Access Django admin at: `http://localhost:8000/admin/`

Login with your superuser credentials.

## API Documentation

Swagger UI is available at: `http://localhost:8000/api/docs/`

## Configuration

### Environment Variables

Backend (.env):
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DATABASE_URL=sqlite:///db.sqlite3
```

Frontend (.env.local):
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Key Features by Role

### Super Admin
- Manage all users and roles
- Manage multiple schools
- View audit logs
- System configuration

### Admin
- Manage classes and subjects
- Manage students and staff
- Configure fees and exams
- View reports and analytics
- Manage transport routes

### Teacher
- Mark attendance
- Enter exam marks
- Create homework assignments
- Maintain class diary
- View assigned classes and students

### Student
- View personal attendance
- Check exam results
- View marks and report cards
- Submit homework
- Access library catalog

### Parent
- View child's attendance
- Track fee payments
- Check exam results and report cards
- Receive notifications
- Submit complaints

### Accountant
- Manage fee structures
- Track fee payments
- Generate invoices
- Manage payroll
- Financial reports

### Transport Manager
- Manage routes and vehicles
- Assign students to routes
- Track driver information
- Monitor transport attendance

## Security Features

- **UUID Primary Keys**: Enhanced security with globally unique identifiers
- **Role-Based Access Control**: Fine-grained permissions per role
- **Audit Logging**: Complete audit trail of all actions
- **Data Encryption**: Ready for SSL/TLS implementation
- **CORS Configuration**: Secure cross-origin requests
- **Token Authentication**: Secure API authentication

## Scalability

The system is designed for scalability:

- **Database**: Easily migrate from SQLite to PostgreSQL/MySQL
- **Caching**: Redis integration ready for performance
- **Async Tasks**: Celery integration ready for background jobs
- **Multi-branch**: Support for multiple school branches

## Future Enhancements

- AI-powered attendance (face recognition)
- GPS tracking for buses
- Mobile app
- Advanced analytics and BI
- Payment gateway integration
- Email and SMS gateway integration
- Video conferencing for online classes

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please contact the development team.

## Deployment

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up proper CORS_ALLOWED_ORIGINS
- [ ] Enable SSL/TLS
- [ ] Set up email backend
- [ ] Configure media storage
- [ ] Set up backup strategy
- [ ] Enable monitoring and logging

### Docker Deployment

Docker configuration coming soon...

### Cloud Deployment

AWS, Azure, and Google Cloud deployment guides coming soon...
