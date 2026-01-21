# Backend Data Fetching - Complete Setup Summary

## Overview
Your School Management System is fully configured to fetch all data from the backend using REST API endpoints only. No direct database access is needed - all operations go through the API.

## Files Created/Updated

### 1. **API_GUIDE.md** - Complete API Documentation
   - All available endpoints
   - Query parameters
   - Response formats
   - Usage examples

### 2. **FETCH_DATA_GUIDE.md** - Practical Guide
   - cURL examples for all endpoints
   - JavaScript/React examples
   - Common query parameters
   - Error handling patterns
   - Best practices

### 3. **frontend/src/services/apiEnhanced.js** - Enhanced API Service
   - **New Features:**
     - Better error handling with token refresh
     - `fetchPaginatedData()` - Fetch with pagination
     - `fetchAllData()` - Fetch all pages automatically
     - Methods for each data type
     - Response interceptors

   - **Methods Added:**
     - `getAllXxx()` methods for each resource
     - Detail methods for single items
     - Search and filter methods

### 4. **frontend/src/components/DataFetchingExample.js** - Example Component
   - 6 different fetching patterns
   - Interactive buttons to test each pattern
   - Error handling display
   - Loading states

### 5. **frontend/src/hooks/useDataFetch.js** - Custom React Hooks
   - `usePaginatedFetch()` - For paginated lists
   - `useAllDataFetch()` - For fetching all data
   - `useItemFetch()` - For single items
   - `useMultipleFetch()` - For multiple parallel requests
   - Ready-to-use component examples

---

## Quick Start Guide

### Step 1: Start the Backend
```bash
cd school-management-system/backend
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

### Step 2: Start the Frontend
```bash
cd school-management-system/frontend
npm install
npm start
```

### Step 3: Use the API

#### Option A: Using cURL (Terminal)
```bash
# Get all students
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/students/
```

#### Option B: Using JavaScript
```javascript
import { schoolApi } from './services/apiEnhanced';

// Fetch all students
const students = await schoolApi.getAllStudents();
console.log(students);
```

#### Option C: Using React Hooks
```javascript
import { useAllDataFetch } from './hooks/useDataFetch';
import { schoolApi } from './services/apiEnhanced';

function MyComponent() {
  const { data: students, loading, error } = useAllDataFetch(
    schoolApi.getAllStudents
  );

  return <div>{students.length} students</div>;
}
```

---

## Available API Endpoints

### Core Resources
- Users: `/users/`, `/users/{id}/`, `/users/profile/`
- Students: `/students/`, `/students/{id}/`, `/students/{id}/attendance/`
- Classes: `/classes/`, `/classes/{id}/`
- Subjects: `/subjects/`, `/subjects/{id}/`
- Parents: `/parents/`, `/parents/{id}/`
- Staff: `/staff/`, `/staff/{id}/`

### Academic
- Academic Years: `/academic-years/`, `/academic-years/active_year/`
- Attendance: `/attendance/`, `/attendance/{id}/`
- Exams: `/exams/`, `/exams/{id}/`
- Marks: `/marks/`, `/marks/{id}/`
- Results: `/results/`, `/results/{id}/`

### Finance
- Fee Structures: `/fee-structures/`, `/fee-structures/{id}/`
- Fee Payments: `/fee-payments/`, `/fee-payments/overdue/`

### Operations
- Transport Routes: `/transport-routes/`, `/transport-routes/{id}/`
- Vehicles: `/vehicles/`, `/vehicles/{id}/`
- Homework: `/homework/`, `/homework/{id}/`
- Notifications: `/notifications/`, `/notifications/unread/`

### Others
- Library Books: `/library-books/`, `/library-books/{id}/`
- Complaints: `/complaints/`, `/complaints/{id}/`
- Certificates: `/certificates/`, `/certificates/{id}/`

---

## Fetching Patterns

### Pattern 1: Fetch Single Page
```javascript
const data = await schoolApi.getStudents({ page: 1, page_size: 10 });
// Returns: { count, next, previous, results }
```

### Pattern 2: Fetch All Data
```javascript
const allData = await schoolApi.getAllStudents();
// Returns: Array of all items (fetches all pages automatically)
```

### Pattern 3: Fetch with Filters
```javascript
const data = await schoolApi.getStudents({ 
  gender: 'MALE',
  current_class: 'uuid',
  search: 'john'
});
```

### Pattern 4: Fetch Specific Item
```javascript
const student = await schoolApi.getStudentDetail('student-uuid');
```

### Pattern 5: Fetch Related Data
```javascript
const attendance = await schoolApi.getStudentAttendance('student-uuid');
const fees = await schoolApi.getStudentFees('student-uuid');
```

### Pattern 6: Parallel Requests
```javascript
const [students, classes, subjects] = await Promise.all([
  schoolApi.getAllStudents(),
  schoolApi.getAllClasses(),
  schoolApi.getAllSubjects()
]);
```

---

## API Features

### ✅ Authentication
- Token-based authentication
- Token automatically added to headers
- 401 errors redirect to login

### ✅ Pagination
- Default page size: 50 items
- Customizable with `page_size` parameter
- Response includes `count`, `next`, `previous`, `results`

### ✅ Filtering
- Filter by model-specific fields
- Search across multiple fields
- Combine filters and search

### ✅ Sorting
- Order by any field using `ordering` parameter
- Prefix with `-` for descending order

### ✅ Error Handling
- Comprehensive error messages
- Status codes (200, 401, 404, 500, etc.)
- Try-catch support

### ✅ CORS
- Enabled for localhost:3000
- Can be configured in settings.py

---

## Common Tasks

### Get All Students
```javascript
const students = await schoolApi.getAllStudents();
```

### Get Students by Gender
```javascript
const maleStudents = await schoolApi.getAllStudents({ gender: 'MALE' });
```

### Search for a Student
```javascript
const results = await schoolApi.getStudents({ search: 'John' });
```

### Get Student's Attendance
```javascript
const attendance = await schoolApi.getStudentAttendance(studentId);
```

### Get Student's Fee Details
```javascript
const fees = await schoolApi.getStudentFees(studentId);
```

### Get All Exams
```javascript
const exams = await schoolApi.getAllExams();
```

### Get All Marks
```javascript
const marks = await schoolApi.getAllMarks();
```

### Get Overdue Payments
```javascript
const overdue = await schoolApi.getOverduePayments();
```

### Get Unread Notifications
```javascript
const unread = await schoolApi.getUnreadNotifications();
```

---

## Development Endpoints

- **Interactive API Docs (Swagger)**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

These are helpful for testing endpoints and understanding response structures.

---

## Environment Configuration

### Backend (.env)
```
DEBUG=True
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## Error Handling

All API calls should include error handling:

```javascript
try {
  const data = await schoolApi.getStudents();
} catch (error) {
  if (error.response?.status === 401) {
    // Unauthorized - redirect to login
  } else if (error.response?.status === 404) {
    // Not found
  } else {
    // Other error
    console.error(error.message);
  }
}
```

---

## Performance Tips

1. **Use `getAllXxx()` for small datasets** - Gets all data at once
2. **Use `getXxx()` with pagination for large datasets** - Implement pagination UI
3. **Cache results** - Store in state/context to avoid repeated calls
4. **Use filters** - Reduce data transfer with query parameters
5. **Batch requests** - Use Promise.all() for multiple requests
6. **Search on backend** - Don't fetch all data then filter locally

---

## Next Steps

1. Test the API with the interactive docs: http://localhost:8000/api/docs/
2. Try the example component: `DataFetchingExample.js`
3. Use custom hooks in your components: `useAllDataFetch`, `usePaginatedFetch`
4. Replace the current API service with `apiEnhanced.js`
5. Build your components using the fetched data

---

## Troubleshooting

### Issue: 401 Unauthorized
**Solution**: Get a valid token and ensure it's stored in localStorage

### Issue: CORS errors
**Solution**: Check CORS_ALLOWED_ORIGINS in settings.py includes your frontend URL

### Issue: Slow pagination
**Solution**: Use filters to reduce data, increase page_size parameter

### Issue: Token not persisting
**Solution**: Check localStorage is available and token is stored after login

---

## Support

For detailed examples and documentation, see:
- `API_GUIDE.md` - Complete API reference
- `FETCH_DATA_GUIDE.md` - Practical fetching examples
- `frontend/src/components/DataFetchingExample.js` - Interactive examples
- `frontend/src/hooks/useDataFetch.js` - Custom hooks with examples

