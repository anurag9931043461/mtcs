# API Quick Reference Card

## Base Setup
```javascript
import { schoolApi, apiUtils } from './services/apiEnhanced';
import { useAllDataFetch, usePaginatedFetch } from './hooks/useDataFetch';
```

---

## Most Common Uses

### Fetch Students List
```javascript
// All students
const students = await schoolApi.getAllStudents();

// Paginated (first page)
const page1 = await schoolApi.getStudents({ page: 1 });

// With React hook
const { data: students } = useAllDataFetch(schoolApi.getAllStudents);
```

### Search/Filter Students
```javascript
// By name
const results = await schoolApi.getStudents({ search: 'John' });

// By gender
const males = await schoolApi.getStudents({ gender: 'MALE' });

// By class
const classStudents = await schoolApi.getStudents({ current_class: 'uuid' });

// Combined
const results = await schoolApi.getStudents({ 
  gender: 'FEMALE', 
  search: 'Jane',
  page: 1
});
```

### Get Single Item
```javascript
const student = await schoolApi.getStudentDetail(studentId);
const exam = await schoolApi.getExamDetail(examId);
const mark = await schoolApi.getMarkDetail(markId);
```

### Student-Related Data
```javascript
const student = await schoolApi.getStudentDetail(id);
const attendance = await schoolApi.getStudentAttendance(id);
const fees = await schoolApi.getStudentFees(id);
```

### Fetch All Classes
```javascript
const classes = await schoolApi.getAllClasses();
```

### Fetch All Subjects
```javascript
const subjects = await schoolApi.getAllSubjects();
```

### Fetch Exams
```javascript
const exams = await schoolApi.getAllExams();
const exam = await schoolApi.getExamDetail(examId);
```

### Fetch Marks/Results
```javascript
const marks = await schoolApi.getAllMarks();
const results = await schoolApi.getAllResults();
```

### Fetch Fee Information
```javascript
const payments = await schoolApi.getAllFeePayments();
const overdue = await schoolApi.getOverduePayments();
const structures = await schoolApi.getAllFeeStructures();
```

### Fetch Attendance
```javascript
const records = await schoolApi.getAllAttendance();
const filtered = await schoolApi.getAttendance({ page: 1 });
```

### Fetch Users/Staff
```javascript
const users = await schoolApi.getAllUsers();
const staff = await schoolApi.getAllStaff();
const parents = await schoolApi.getAllParents();
```

### Fetch Notifications
```javascript
const notifications = await schoolApi.getAllNotifications();
const unread = await schoolApi.getUnreadNotifications();
```

### Fetch Transport
```javascript
const routes = await schoolApi.getAllTransportRoutes();
const vehicles = await schoolApi.getAllVehicles();
```

### Get Current User
```javascript
const profile = await schoolApi.getUserProfile();
```

### Get Active Academic Year
```javascript
const activeYear = await schoolApi.getActiveAcademicYear();
```

---

## React Component Template

### Using Hooks
```javascript
import React from 'react';
import { useAllDataFetch } from './hooks/useDataFetch';
import { schoolApi } from './services/apiEnhanced';

export function StudentsList() {
  const { data: students, loading, error } = useAllDataFetch(
    schoolApi.getAllStudents
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Students ({students.length})</h1>
      <ul>
        {students.map(s => (
          <li key={s.id}>{s.user?.first_name} {s.user?.last_name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Using Effects
```javascript
import React, { useEffect, useState } from 'react';
import { schoolApi } from './services/apiEnhanced';

export function StudentsList() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const data = await schoolApi.getAllStudents();
        setStudents(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {students.map(s => (
        <li key={s.id}>{s.user?.first_name}</li>
      ))}
    </ul>
  );
}
```

---

## All Available Methods

### Students
`getStudents()` `getAllStudents()` `getStudentDetail()` `getStudentAttendance()` `getStudentFees()`

### Classes
`getClasses()` `getAllClasses()` `getClassDetail()`

### Subjects
`getSubjects()` `getAllSubjects()` `getSubjectDetail()`

### Users
`getUsers()` `getAllUsers()` `getUserProfile()` `getUserDetail()`

### Parents
`getParents()` `getAllParents()` `getParentDetail()`

### Staff
`getStaff()` `getAllStaff()` `getStaffDetail()`

### Attendance
`getAttendance()` `getAllAttendance()` `getAttendanceDetail()`

### Exams
`getExams()` `getAllExams()` `getExamDetail()`

### Marks
`getMarks()` `getAllMarks()` `getMarkDetail()`

### Results
`getResults()` `getAllResults()` `getResultDetail()`

### Fees
`getFeeStructures()` `getAllFeeStructures()` `getFeePayments()` `getAllFeePayments()` `getOverduePayments()`

### Academic Years
`getAcademicYears()` `getAllAcademicYears()` `getActiveAcademicYear()`

### Transport
`getTransportRoutes()` `getAllTransportRoutes()` `getVehicles()` `getAllVehicles()`

### Notifications
`getNotifications()` `getAllNotifications()` `getUnreadNotifications()`

### Library
`getLibraryBooks()` `getAllLibraryBooks()` `getLibraryBookDetail()`

### Complaints
`getComplaints()` `getAllComplaints()`

### Certificates
`getCertificates()` `getAllCertificates()`

---

## Custom Hooks Reference

### usePaginatedFetch
```javascript
const { data, loading, error, page, setPage, hasMore } = usePaginatedFetch(
  schoolApi.getStudents,
  { page_size: 20 }
);
```

### useAllDataFetch
```javascript
const { data, loading, error, refetch } = useAllDataFetch(
  schoolApi.getAllStudents
);
```

### useItemFetch
```javascript
const { data, loading, error } = useItemFetch(
  schoolApi.getStudentDetail,
  studentId
);
```

### useMultipleFetch
```javascript
const { data, loading, error } = useMultipleFetch([
  { key: 'students', method: schoolApi.getAllStudents },
  { key: 'classes', method: schoolApi.getAllClasses }
]);
```

---

## Query Parameters

```javascript
// Pagination
{ page: 1, page_size: 50 }

// Search
{ search: 'John' }

// Filter
{ gender: 'MALE', current_class: 'uuid' }

// Sorting
{ ordering: 'name' }              // Ascending
{ ordering: '-created_at' }       // Descending

// Combined
{ search: 'John', gender: 'MALE', page: 1, page_size: 20 }
```

---

## Error Handling
```javascript
try {
  const data = await schoolApi.getAllStudents();
} catch (error) {
  console.error('API Error:', error.message);
  // Handle error
}
```

---

## Quick cURL Examples
```bash
TOKEN="your_token"

# All students
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/students/

# Male students
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/students/?gender=MALE

# Search
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/students/?search=John

# Specific student
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/students/UUID/

# Attendance
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/students/UUID/attendance/

# All classes
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/classes/

# All exams
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/exams/
```

---

## Response Structure

### List Response
```javascript
{
  count: 150,           // Total items
  next: "url",          // Next page URL
  previous: null,       // Previous page URL
  results: [...]        // Array of items
}
```

### Single Item Response
```javascript
{
  id: "uuid",
  name: "...",
  // other fields
}
```

---

## Tips

✅ Use `getAllXxx()` for small/medium datasets  
✅ Use `getXxx()` with pagination for large datasets  
✅ Cache results in state/context  
✅ Use filters to reduce data  
✅ Batch requests with Promise.all()  
✅ Always handle errors with try-catch  
✅ Check React DevTools to debug hooks  

---

## Links

📚 **Full Documentation**: See `API_GUIDE.md`  
📖 **Examples**: See `FETCH_DATA_GUIDE.md`  
🎯 **Component Examples**: See `frontend/src/components/DataFetchingExample.js`  
🪝 **Custom Hooks**: See `frontend/src/hooks/useDataFetch.js`  
🌐 **API Docs (Interactive)**: http://localhost:8000/api/docs/
