# API Usage Guide - Fetch Data from Backend

## Quick Start

### Get Your Token
First, you need to authenticate and get your API token.

**Login (POST)**
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

Or if using Django TokenAuthentication:
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

### Use Token in Requests
Save your token and use it in the `Authorization` header:
```bash
export TOKEN="your_token_here"
curl -H "Authorization: Token $TOKEN" \
  http://localhost:8000/api/students/
```

---

## Fetching Data - cURL Examples

### 1. Fetch All Students (Paginated)
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/?page=1"
```

### 2. Fetch Students with Filters
```bash
# By class
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/?current_class=UUID"

# By gender
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/?gender=MALE"

# Search by name
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/?search=John"

# Multiple filters
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/?gender=FEMALE&search=Jane&page=1"
```

### 3. Fetch Specific Student
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/UUID/"
```

### 4. Fetch Student Attendance
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/UUID/attendance/"
```

### 5. Fetch Student Fee Details
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/students/UUID/fee_details/"
```

### 6. Fetch All Classes
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/classes/"
```

### 7. Fetch All Subjects
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/subjects/"
```

### 8. Fetch Attendance Records
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/attendance/"
```

### 9. Fetch Fee Payments
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/fee-payments/"
```

### 10. Fetch Overdue Payments
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/fee-payments/overdue/"
```

### 11. Fetch All Exams
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/exams/"
```

### 12. Fetch All Marks
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/marks/"
```

### 13. Fetch User Profile
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/users/profile/"
```

### 14. Fetch Active Academic Year
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/academic-years/active_year/"
```

### 15. Fetch Notifications
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/notifications/"
```

### 16. Fetch Unread Notifications
```bash
curl -H "Authorization: Token $TOKEN" \
  "http://localhost:8000/api/notifications/unread/"
```

---

## Fetching Data - JavaScript/React Examples

### Using the Enhanced API Service

#### Example 1: Fetch Paginated Data
```javascript
import { schoolApi } from './services/apiEnhanced';

// Fetch first page
const data = await schoolApi.getStudents({ page: 1, page_size: 10 });
console.log(data.results); // Array of students
console.log(data.count);   // Total count
console.log(data.next);    // URL to next page
```

#### Example 2: Fetch All Data (All Pages)
```javascript
import { schoolApi } from './services/apiEnhanced';

// Automatically fetches all pages
const allStudents = await schoolApi.getAllStudents();
console.log(allStudents.length); // Total students
```

#### Example 3: Fetch with Filters
```javascript
import { schoolApi } from './services/apiEnhanced';

// Filter by multiple criteria
const students = await schoolApi.getStudents({ 
  current_class: 'class-uuid',
  gender: 'MALE',
  page: 1,
  page_size: 20
});
```

#### Example 4: Fetch Specific Item
```javascript
import { schoolApi } from './services/apiEnhanced';

const student = await schoolApi.getStudentDetail('student-uuid');
console.log(student);
```

#### Example 5: Fetch Multiple Resources in Parallel
```javascript
import { schoolApi } from './services/apiEnhanced';

const [students, classes, subjects] = await Promise.all([
  schoolApi.getAllStudents(),
  schoolApi.getAllClasses(),
  schoolApi.getAllSubjects()
]);
```

#### Example 6: Fetch with Search
```javascript
import { schoolApi } from './services/apiEnhanced';

const results = await schoolApi.getStudents({ 
  search: 'John',
  page_size: 50
});
```

#### Example 7: React Component - Fetch Data on Mount
```javascript
import React, { useEffect, useState } from 'react';
import { schoolApi } from '../services/apiEnhanced';

function StudentsList() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const data = await schoolApi.getAllStudents();
        setStudents(data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  
  return (
    <div>
      <h1>Students ({students.length})</h1>
      <ul>
        {students.map(student => (
          <li key={student.id}>
            {student.user?.first_name} {student.user?.last_name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StudentsList;
```

---

## Common Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `page` | Page number | `?page=1` |
| `page_size` | Items per page | `?page_size=50` |
| `search` | Search term | `?search=John` |
| `ordering` | Sort field (prefix with `-` for desc) | `?ordering=-created_at` |
| Filter fields | Model-specific filters | `?gender=MALE&role=STUDENT` |

## Response Format

### Paginated Response
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-123",
      "roll_number": "001",
      "user": {
        "id": "user-uuid",
        "username": "student1",
        "first_name": "John",
        "last_name": "Doe"
      },
      "gender": "MALE",
      "current_class": "class-uuid"
    }
  ]
}
```

### Single Item Response
```json
{
  "id": "uuid-123",
  "roll_number": "001",
  "user": {...},
  "gender": "MALE",
  "current_class": "class-uuid",
  "admission_number": "ADM001",
  "date_of_birth": "2010-05-15"
}
```

---

## Error Handling

### Error Response
```json
{
  "detail": "Not found.",
  "error": "Invalid request"
}
```

### JavaScript Error Handling
```javascript
import { schoolApi } from './services/apiEnhanced';

try {
  const data = await schoolApi.getStudents();
} catch (error) {
  if (error.response?.status === 401) {
    console.log('Unauthorized - need to login');
  } else if (error.response?.status === 404) {
    console.log('Resource not found');
  } else {
    console.log('Error:', error.message);
  }
}
```

---

## API Service Methods Reference

### Students
- `getStudents(params)` - Fetch paginated students
- `getAllStudents(params)` - Fetch all students
- `getStudentDetail(id)` - Get specific student
- `getStudentAttendance(id)` - Get student attendance
- `getStudentFees(id)` - Get student fees

### Classes
- `getClasses(params)` - Fetch classes
- `getAllClasses(params)` - Fetch all classes
- `getClassDetail(id)` - Get specific class

### Subjects
- `getSubjects(params)` - Fetch subjects
- `getAllSubjects(params)` - Fetch all subjects

### Attendance
- `getAttendance(params)` - Fetch attendance records
- `getAllAttendance(params)` - Fetch all attendance

### Fees
- `getFeePayments(params)` - Fetch fee payments
- `getAllFeePayments(params)` - Fetch all payments
- `getOverduePayments()` - Get overdue payments

### Exams & Marks
- `getExams(params)` - Fetch exams
- `getMarks(params)` - Fetch marks
- `getResults(params)` - Fetch results

### Users
- `getUsers(params)` - Fetch users
- `getUserProfile()` - Get current user profile
- `getUserDetail(id)` - Get specific user

---

## Environment Variables

Set these in your `.env` file:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## Interactive API Documentation

Visit the interactive docs while the backend is running:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## Tips & Best Practices

1. **Use getAllXxx() for small datasets** - Gets all data at once
2. **Use getXxx() for large datasets** - Implement pagination yourself
3. **Always handle errors** - Use try-catch blocks
4. **Cache results** - Store fetched data in state/context
5. **Use filters** - Reduce data transfer with query parameters
6. **Batch requests** - Use Promise.all() for multiple requests
7. **Check token** - Ensure token is in localStorage before making requests

