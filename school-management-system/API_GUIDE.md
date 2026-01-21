# School Management System - API Documentation

## Overview
The backend provides a comprehensive REST API for all school management operations. All data is fetched through API endpoints only.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Token-based authentication is used. Include the token in the Authorization header:
```
Authorization: Token <your_token_here>
```

## Available Endpoints

### 1. Users
- **GET** `/users/` - List all users
  - Query params: `role`, `is_active`, `search`, `ordering`
  - Example: `/users/?role=STUDENT&is_active=true`

- **GET** `/users/{id}/` - Get user detail
- **POST** `/users/` - Create new user
- **PUT** `/users/{id}/` - Update user
- **DELETE** `/users/{id}/` - Delete user
- **GET** `/users/profile/` - Get current user profile

### 2. Academic Years
- **GET** `/academic-years/` - List all academic years
- **GET** `/academic-years/{id}/` - Get academic year detail
- **POST** `/academic-years/` - Create academic year
- **GET** `/academic-years/active_year/` - Get active academic year

### 3. Schools
- **GET** `/schools/` - List all schools
- **GET** `/schools/{id}/` - Get school detail
- **POST** `/schools/` - Create school

### 4. Classes
- **GET** `/classes/` - List all classes
  - Query params: `academic_year`, `class_number`, `search`
- **GET** `/classes/{id}/` - Get class detail
- **POST** `/classes/` - Create class

### 5. Subjects
- **GET** `/subjects/` - List all subjects
  - Query params: `search`
- **POST** `/subjects/` - Create subject

### 6. Students
- **GET** `/students/` - List all students
  - Query params: `current_class`, `gender`, `search`
  - Example: `/students/?gender=MALE&search=John`
- **GET** `/students/{id}/` - Get student detail
- **GET** `/students/{id}/attendance/` - Get student attendance
- **GET** `/students/{id}/fee_details/` - Get student fee payments
- **POST** `/students/` - Create student
- **PUT** `/students/{id}/` - Update student

### 7. Parents
- **GET** `/parents/` - List all parents
- **GET** `/parents/{id}/` - Get parent detail

### 8. Staff
- **GET** `/staff/` - List all staff members
- **GET** `/staff/{id}/` - Get staff detail

### 9. Attendance
- **GET** `/attendance/` - List attendance records
- **POST** `/attendance/` - Mark attendance
- **POST** `/attendance/bulk_mark/` - Bulk mark attendance
- **PUT** `/attendance/{id}/` - Update attendance

### 10. Fee Management
- **GET** `/fee-structures/` - List fee structures
- **GET** `/fee-payments/` - List fee payments
- **GET** `/fee-payments/overdue/` - Get overdue payments
- **POST** `/fee-payments/` - Create fee payment
- **PUT** `/fee-payments/{id}/` - Update fee payment

### 11. Exams
- **GET** `/exams/` - List all exams
- **GET** `/exams/{id}/` - Get exam detail
- **POST** `/exams/` - Create exam
- **POST** `/exams/{id}/publish_results/` - Publish exam results

### 12. Marks
- **GET** `/marks/` - List marks
- **POST** `/marks/` - Create mark
- **PUT** `/marks/{id}/` - Update mark
- **POST** `/marks/bulk_upload/` - Bulk upload marks

### 13. Results
- **GET** `/results/` - List results
- **GET** `/results/{id}/` - Get result detail

### 14. Transport
- **GET** `/transport-routes/` - List transport routes
- **GET** `/vehicles/` - List vehicles
- **POST** `/vehicles/` - Create vehicle

### 15. Homework
- **GET** `/homework/` - List homework
- **POST** `/homework/` - Create homework
- **PUT** `/homework/{id}/` - Update homework

### 16. Notifications
- **GET** `/notifications/` - List notifications
- **GET** `/notifications/unread/` - Get unread notifications
- **POST** `/notifications/` - Create notification

### 17. Library
- **GET** `/library-books/` - List library books
- **GET** `/library-books/{id}/` - Get book detail

### 18. Complaints
- **GET** `/complaints/` - List complaints
- **POST** `/complaints/` - Create complaint
- **PUT** `/complaints/{id}/` - Update complaint

### 19. Certificates
- **GET** `/certificates/` - List certificates
- **GET** `/certificates/{id}/` - Get certificate detail

## Query Parameters

### Common Query Parameters
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 50)
- `search` - Search term
- `ordering` - Field to order by (prefix with `-` for descending)

### Response Format
All responses return JSON:

**Success Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "user": {...},
      "roll_number": "001",
      ...
    }
  ]
}
```

**Error Response (4xx/5xx):**
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Usage Examples

### Fetch All Students
```javascript
fetch('http://localhost:8000/api/students/', {
  headers: {
    'Authorization': 'Token your_token_here'
  }
})
.then(res => res.json())
.then(data => console.log(data.results))
```

### Fetch with Filters
```javascript
fetch('http://localhost:8000/api/students/?current_class=uuid&gender=MALE', {
  headers: {
    'Authorization': 'Token your_token_here'
  }
})
.then(res => res.json())
.then(data => console.log(data.results))
```

### Fetch Specific Item
```javascript
fetch('http://localhost:8000/api/students/uuid-id/', {
  headers: {
    'Authorization': 'Token your_token_here'
  }
})
.then(res => res.json())
.then(data => console.log(data))
```

## CORS Configuration
CORS is enabled for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## Documentation
- **Interactive API Docs**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Pagination
All list endpoints support pagination. Default page size is 50 items.

Example:
```
GET /api/students/?page=1
GET /api/students/?page=2&page_size=100
```
