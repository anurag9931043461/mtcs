import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add authorization token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const schoolApi = {
  // Users
  getUsers: (params) => apiClient.get('/users/', { params }),
  getUserProfile: () => apiClient.get('/users/profile/'),
  createUser: (data) => apiClient.post('/users/', data),
  updateUser: (id, data) => apiClient.put(`/users/${id}/`, data),
  deleteUser: (id) => apiClient.delete(`/users/${id}/`),

  // Students
  getStudents: (params) => apiClient.get('/students/', { params }),
  getStudentDetail: (id) => apiClient.get(`/students/${id}/`),
  getStudentAttendance: (id) => apiClient.get(`/students/${id}/attendance/`),
  getStudentFees: (id) => apiClient.get(`/students/${id}/fee_details/`),
  createStudent: (data) => apiClient.post('/students/', data),
  updateStudent: (id, data) => apiClient.put(`/students/${id}/`, data),

  // Classes
  getClasses: (params) => apiClient.get('/classes/', { params }),
  getClassDetail: (id) => apiClient.get(`/classes/${id}/`),
  createClass: (data) => apiClient.post('/classes/', data),
  updateClass: (id, data) => apiClient.put(`/classes/${id}/`, data),

  // Subjects
  getSubjects: (params) => apiClient.get('/subjects/', { params }),
  createSubject: (data) => apiClient.post('/subjects/', data),
  updateSubject: (id, data) => apiClient.put(`/subjects/${id}/`, data),

  // Attendance
  getAttendance: (params) => apiClient.get('/attendance/', { params }),
  markAttendance: (data) => apiClient.post('/attendance/', data),
  bulkMarkAttendance: (data) => apiClient.post('/attendance/bulk_mark/', data),
  updateAttendance: (id, data) => apiClient.put(`/attendance/${id}/`, data),

  // Fees
  getFeeStructures: (params) => apiClient.get('/fee-structures/', { params }),
  getFeePayments: (params) => apiClient.get('/fee-payments/', { params }),
  getOverduePayments: () => apiClient.get('/fee-payments/overdue/'),
  createFeePayment: (data) => apiClient.post('/fee-payments/', data),
  updateFeePayment: (id, data) => apiClient.put(`/fee-payments/${id}/`, data),

  // Exams
  getExams: (params) => apiClient.get('/exams/', { params }),
  getExamDetail: (id) => apiClient.get(`/exams/${id}/`),
  createExam: (data) => apiClient.post('/exams/', data),
  publishResults: (id) => apiClient.post(`/exams/${id}/publish_results/`),

  // Marks
  getMarks: (params) => apiClient.get('/marks/', { params }),
  createMark: (data) => apiClient.post('/marks/', data),
  updateMark: (id, data) => apiClient.put(`/marks/${id}/`, data),
  bulkUploadMarks: (data) => apiClient.post('/marks/bulk_upload/', data),

  // Results
  getResults: (params) => apiClient.get('/results/', { params }),
  getResultDetail: (id) => apiClient.get(`/results/${id}/`),

  // Transport
  getTransportRoutes: (params) => apiClient.get('/transport-routes/', { params }),
  getVehicles: (params) => apiClient.get('/vehicles/', { params }),
  createVehicle: (data) => apiClient.post('/vehicles/', data),
  updateVehicle: (id, data) => apiClient.put(`/vehicles/${id}/`, data),

  // Homework
  getHomework: (params) => apiClient.get('/homework/', { params }),
  createHomework: (data) => apiClient.post('/homework/', data),
  updateHomework: (id, data) => apiClient.put(`/homework/${id}/`, data),

  // Notifications
  getNotifications: (params) => apiClient.get('/notifications/', { params }),
  getUnreadNotifications: () => apiClient.get('/notifications/unread/'),
  createNotification: (data) => apiClient.post('/notifications/', data),

  // Library
  getLibraryBooks: (params) => apiClient.get('/library-books/', { params }),
  getBookDetail: (id) => apiClient.get(`/library-books/${id}/`),

  // Complaints
  getComplaints: (params) => apiClient.get('/complaints/', { params }),
  createComplaint: (data) => apiClient.post('/complaints/', data),
  updateComplaint: (id, data) => apiClient.put(`/complaints/${id}/`, data),

  // Certificates
  getCertificates: (params) => apiClient.get('/certificates/', { params }),
  createCertificate: (data) => apiClient.post('/certificates/', data),

  // Academic Years
  getAcademicYears: () => apiClient.get('/academic-years/'),
  getActiveAcademicYear: () => apiClient.get('/academic-years/active_year/'),
};

export default apiClient;
