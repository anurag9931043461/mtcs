# 🔒 API-ONLY DATA FETCHING - Enforcement Guide

## ⚠️ Critical Rule

**ALL data in the frontend MUST come from the backend API ONLY**

✅ **ALLOWED**: HTTP API calls to backend  
❌ **NOT ALLOWED**:
- Hardcoded data
- Dummy data for testing
- Direct database queries
- Local storage of data (only for tokens/auth)
- Mock data
- Fake data structures

---

## ✅ Implementation Checklist

### 1. **Authentication API** - MUST USE
Every login must call the backend API:

```javascript
// ❌ WRONG
const handleLogin = (username, password) => {
  login('dummy-token', { username, first_name: 'Admin' }); // Hardcoded!
};

// ✅ CORRECT
const handleLogin = async (username, password) => {
  try {
    const response = await apiClient.post('/auth/login/', { username, password });
    login(response.data.token, response.data.user);
  } catch (error) {
    setError(error.message);
  }
};
```

### 2. **Dashboard Stats** - MUST FETCH FROM API
Every statistic must come from an API endpoint:

```javascript
// ❌ WRONG
<p className="text-2xl font-bold">450</p>  // Hardcoded number!

// ✅ CORRECT
const Dashboard = () => {
  const [stats, setStats] = useState({ students: 0, teachers: 0 });
  
  useEffect(() => {
    Promise.all([
      schoolApi.getAllStudents().then(data => data.length),
      schoolApi.getAllStaff().then(data => data.length)
    ]).then(([studentCount, teacherCount]) => {
      setStats({ students: studentCount, teachers: teacherCount });
    });
  }, []);
  
  return <p className="text-2xl font-bold">{stats.students}</p>;
};
```

### 3. **Lists & Tables** - MUST FETCH FROM API
Every list must call the API:

```javascript
// ❌ WRONG
setStudents([
  { id: 1, name: 'John' }, // Hardcoded!
  { id: 2, name: 'Jane' }
]);

// ✅ CORRECT
useEffect(() => {
  schoolApi.getAllStudents().then(setStudents);
}, []);
```

### 4. **Forms & Operations** - MUST USE API
Every create/update/delete must use the API:

```javascript
// ❌ WRONG
const handleAddStudent = () => {
  setIsModalOpen(false); // Just closes modal, no API call!
};

// ✅ CORRECT
const handleAddStudent = async (formData) => {
  try {
    await schoolApi.createStudent(formData);
    setIsModalOpen(false);
    fetchStudents(); // Refresh from API
  } catch (error) {
    setError(error.message);
  }
};
```

---

## 🔄 Data Flow (Required Pattern)

```
User Action
    ↓
Component Event
    ↓
API Call (schoolApi.xxxx())
    ↓
Backend Processing
    ↓
API Response
    ↓
Update Component State
    ↓
Re-render UI

❌ NO SHORTCUTS - Always follow this pattern
```

---

## 📋 File Enforcement Rules

### LoginPage.js
```javascript
// Rule 1: Authentication MUST use API
const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('/api/token-auth/', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    login(data.token, data.user);
  } catch (error) {
    setError('Login failed');
  }
};
```

### Dashboard.js
```javascript
// Rule 2: Stats MUST be fetched from API
useEffect(() => {
  (async () => {
    const [students, staff, classes] = await Promise.all([
      schoolApi.getAllStudents(),
      schoolApi.getAllStaff(),
      schoolApi.getAllClasses()
    ]);
    setStats({
      students: students.length,
      staff: staff.length,
      classes: classes.length
    });
  })();
}, []);
```

### StudentsList.js
```javascript
// Rule 3: Data MUST be fetched from API
useEffect(() => {
  fetchStudents();
}, []);

const fetchStudents = async () => {
  try {
    setLoading(true);
    const data = await schoolApi.getAllStudents();
    setStudents(data);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};

// Rule 4: Create operations MUST use API
const handleAddStudent = async (formData) => {
  try {
    await schoolApi.createStudent(formData);
    await fetchStudents(); // Refresh from API
  } catch (error) {
    setError(error.message);
  }
};
```

---

## 🚫 What to Remove/Never Do

### ❌ Remove Hardcoded Data
```javascript
// DELETE THIS:
const dummyData = [
  { id: 1, name: 'John' },
  { id: 2, name: 'Jane' }
];
setStudents(dummyData);
```

### ❌ Remove Fake Numbers
```javascript
// DELETE THIS:
<p>Total Students: 450</p>
<p>Total Teachers: 35</p>
<p>Total Classes: 12</p>
```

### ❌ Remove Mock Functions
```javascript
// DELETE THIS:
const mockFetch = () => {
  return Promise.resolve({ data: [...] });
};
```

### ❌ Never Skip API Calls
```javascript
// ❌ WRONG - No API call!
const handleSubmit = () => {
  setIsModalOpen(false);
  // Where's the API call?
};

// ✅ CORRECT - Uses API!
const handleSubmit = async (data) => {
  await schoolApi.createStudent(data);
  setIsModalOpen(false);
};
```

---

## ✨ Correct API-Only Pattern

### 1. Component Setup
```javascript
import { useAllDataFetch } from '../hooks/useDataFetch';
import { schoolApi } from '../services/apiEnhanced';

function MyComponent() {
  const { data, loading, error } = useAllDataFetch(
    schoolApi.getAllStudents
  );

  if (loading) return <div>Loading from API...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return <div>{data.length} students</div>;
}
```

### 2. Manual Fetch Pattern
```javascript
function MyComponent() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await schoolApi.getAllStudents();
        setStudents(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return <div>{students.map(s => <div key={s.id}>{s.name}</div>)}</div>;
}
```

### 3. Create/Update Pattern
```javascript
const handleCreate = async (formData) => {
  try {
    setLoading(true);
    await schoolApi.createStudent(formData);
    // Refresh data from API
    const updated = await schoolApi.getAllStudents();
    setStudents(updated);
    setIsModalOpen(false);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};
```

---

## 🔐 Enforcement Rules

### Rule 1: Every Page Load
- MUST fetch data from API
- NO hardcoded/dummy data
- Show loading state while fetching
- Handle errors gracefully

### Rule 2: Every User Action
- Create → API call → Refresh from API
- Update → API call → Refresh from API
- Delete → API call → Refresh from API
- List → API call → Display

### Rule 3: No Exceptions
- Token storage (localStorage) - ✅ ALLOWED
- Error messages (local state) - ✅ ALLOWED
- UI state (modals, forms) - ✅ ALLOWED
- **Data** (students, classes, etc.) - ❌ NOT LOCAL, MUST BE FROM API

### Rule 4: Error Handling
```javascript
try {
  const data = await schoolApi.getAllStudents();
  setStudents(data);
} catch (error) {
  // Handle 401 - redirect to login
  if (error.response?.status === 401) {
    window.location.href = '/login';
  }
  // Handle other errors
  setError(error.message);
}
```

---

## 📝 Code Review Checklist

Before committing code:
- [ ] No hardcoded data arrays?
- [ ] No dummy numbers/strings?
- [ ] All data from `schoolApi.*` methods?
- [ ] Error handling for API calls?
- [ ] Loading states shown?
- [ ] API called on component mount?
- [ ] API called after create/update/delete?
- [ ] No localStorage for business data?
- [ ] Token-based auth only?

---

## 🚨 Common Mistakes to Avoid

### Mistake 1: Hardcoded Data
```javascript
// ❌ WRONG
const data = [{ id: 1, name: 'John' }];

// ✅ CORRECT
const data = await schoolApi.getAllStudents();
```

### Mistake 2: No API Refresh After Action
```javascript
// ❌ WRONG
await schoolApi.createStudent(data);
setIsModalOpen(false);
// No data refresh!

// ✅ CORRECT
await schoolApi.createStudent(data);
const updated = await schoolApi.getAllStudents();
setStudents(updated);
setIsModalOpen(false);
```

### Mistake 3: Storing Business Data Locally
```javascript
// ❌ WRONG
localStorage.setItem('students', JSON.stringify(students));

// ✅ CORRECT
// Always fetch fresh from API
const students = await schoolApi.getAllStudents();
```

### Mistake 4: Dummy Login
```javascript
// ❌ WRONG
login('dummy-token', { name: 'Admin' });

// ✅ CORRECT
const response = await apiClient.post('/auth/login/', { username, password });
login(response.data.token, response.data.user);
```

### Mistake 5: Skipping Error Handling
```javascript
// ❌ WRONG
const data = await schoolApi.getAllStudents();
setStudents(data);

// ✅ CORRECT
try {
  const data = await schoolApi.getAllStudents();
  setStudents(data);
} catch (error) {
  setError(error.message);
}
```

---

## 📚 Required API Methods

Every component should use these patterns:

```javascript
// ✅ List with hook
const { data } = useAllDataFetch(schoolApi.getAllStudents);

// ✅ List manual
const data = await schoolApi.getAllStudents();

// ✅ Paginated list
const result = await schoolApi.getStudents({ page: 1 });

// ✅ Single item
const item = await schoolApi.getStudentDetail(id);

// ✅ Create
await schoolApi.createStudent(data);

// ✅ Update
await schoolApi.updateStudent(id, data);

// ✅ Delete
await schoolApi.deleteStudent(id);

// ✅ Get related data
const attendance = await schoolApi.getStudentAttendance(id);
```

---

## 🎯 Summary

**Remember: ALL data flows through the API**

```
         Backend API
              ↑
              | HTTP
              |
        Frontend React App
        ├─ Components (UI)
        ├─ State (state, props)
        ├─ Hooks (custom, react)
        └─ Services (API calls)
             ↓
         localStorage (tokens only!)
```

**Never bypass the API!**

---

## ✅ Implementation Complete

All components must follow these rules:
- ✅ Authentication from API
- ✅ Lists from API
- ✅ Details from API
- ✅ Stats from API
- ✅ Create from API
- ✅ Update from API
- ✅ Delete from API
- ✅ Search from API
- ✅ Filter from API

**100% API-driven frontend**
