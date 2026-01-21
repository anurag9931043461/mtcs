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

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Generic function to fetch paginated data
 * @param {string} endpoint - API endpoint
 * @param {object} params - Query parameters
 * @returns {Promise} Response with data
 */
const fetchPaginatedData = async (endpoint, params = {}) => {
  try {
    const response = await apiClient.get(endpoint, { params });
    return response.data;
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    throw error;
  }
};

/**
 * Generic function to fetch all data (all pages)
 * @param {string} endpoint - API endpoint
 * @param {object} params - Query parameters
 * @returns {Promise} Array of all results
 */
const fetchAllData = async (endpoint, params = {}) => {
  try {
    let allResults = [];
    let nextUrl = null;
    let page = 1;

    do {
      const response = await apiClient.get(endpoint, { 
        params: { ...params, page, page_size: 100 } 
      });
      allResults = [...allResults, ...response.data.results];
      nextUrl = response.data.next;
      page++;
    } while (nextUrl);

    return allResults;
  } catch (error) {
    console.error(`Error fetching all data from ${endpoint}:`, error);
    throw error;
  }
};

export const schoolApi = {
  // ============= Users =============
  getUsers: (params) => fetchPaginatedData('/users/', params),
  getAllUsers: (params) => fetchAllData('/users/', params),
  getUserProfile: () => apiClient.get('/users/profile/'),
  getUserDetail: (id) => apiClient.get(`/users/${id}/`),
  createUser: (data) => apiClient.post('/users/', data),
  updateUser: (id, data) => apiClient.put(`/users/${id}/`, data),
  deleteUser: (id) => apiClient.delete(`/users/${id}/`),

  // ============= Students =============
  getStudents: (params) => fetchPaginatedData('/students/', params),
  getAllStudents: (params) => fetchAllData('/students/', params),
  getStudentDetail: (id) => apiClient.get(`/students/${id}/`),
  getStudentAttendance: (id) => apiClient.get(`/students/${id}/attendance/`),
  getStudentFees: (id) => apiClient.get(`/students/${id}/fee_details/`),
  createStudent: (data) => apiClient.post('/students/', data),
  updateStudent: (id, data) => apiClient.put(`/students/${id}/`, data),
  deleteStudent: (id) => apiClient.delete(`/students/${id}/`),

  // ============= Parents =============
  getParents: (params) => fetchPaginatedData('/parents/', params),
  getAllParents: (params) => fetchAllData('/parents/', params),
  getParentDetail: (id) => apiClient.get(`/parents/${id}/`),
  createParent: (data) => apiClient.post('/parents/', data),
  updateParent: (id, data) => apiClient.put(`/parents/${id}/`, data),

  // ============= Staff =============
  getStaff: (params) => fetchPaginatedData('/staff/', params),
  getAllStaff: (params) => fetchAllData('/staff/', params),
  getStaffDetail: (id) => apiClient.get(`/staff/${id}/`),
  createStaff: (data) => apiClient.post('/staff/', data),
  updateStaff: (id, data) => apiClient.put(`/staff/${id}/`, data),

  // ============= Classes =============
  getClasses: (params) => fetchPaginatedData('/classes/', params),
  getAllClasses: (params) => fetchAllData('/classes/', params),
  getClassDetail: (id) => apiClient.get(`/classes/${id}/`),
  createClass: (data) => apiClient.post('/classes/', data),
  updateClass: (id, data) => apiClient.put(`/classes/${id}/`, data),

  // ============= Subjects =============
  getSubjects: (params) => fetchPaginatedData('/subjects/', params),
  getAllSubjects: (params) => fetchAllData('/subjects/', params),
  getSubjectDetail: (id) => apiClient.get(`/subjects/${id}/`),
  createSubject: (data) => apiClient.post('/subjects/', data),
  updateSubject: (id, data) => apiClient.put(`/subjects/${id}/`, data),

  // ============= Academic Years =============
  getAcademicYears: (params) => fetchPaginatedData('/academic-years/', params),
  getAllAcademicYears: (params) => fetchAllData('/academic-years/', params),
  getActiveAcademicYear: () => apiClient.get('/academic-years/active_year/'),
  createAcademicYear: (data) => apiClient.post('/academic-years/', data),
  updateAcademicYear: (id, data) => apiClient.put(`/academic-years/${id}/`, data),

  // ============= Schools =============
  getSchools: (params) => fetchPaginatedData('/schools/', params),
  getAllSchools: (params) => fetchAllData('/schools/', params),
  getSchoolDetail: (id) => apiClient.get(`/schools/${id}/`),
  createSchool: (data) => apiClient.post('/schools/', data),
  updateSchool: (id, data) => apiClient.put(`/schools/${id}/`, data),

  // ============= Attendance =============
  getAttendance: (params) => fetchPaginatedData('/attendance/', params),
  getAllAttendance: (params) => fetchAllData('/attendance/', params),
  getAttendanceDetail: (id) => apiClient.get(`/attendance/${id}/`),
  markAttendance: (data) => apiClient.post('/attendance/', data),
  bulkMarkAttendance: (data) => apiClient.post('/attendance/bulk_mark/', data),
  updateAttendance: (id, data) => apiClient.put(`/attendance/${id}/`, data),

  // ============= Fee Structures =============
  getFeeStructures: (params) => fetchPaginatedData('/fee-structures/', params),
  getAllFeeStructures: (params) => fetchAllData('/fee-structures/', params),
  getFeeStructureDetail: (id) => apiClient.get(`/fee-structures/${id}/`),
  createFeeStructure: (data) => apiClient.post('/fee-structures/', data),
  updateFeeStructure: (id, data) => apiClient.put(`/fee-structures/${id}/`, data),

  // ============= Fee Payments =============
  getFeePayments: (params) => fetchPaginatedData('/fee-payments/', params),
  getAllFeePayments: (params) => fetchAllData('/fee-payments/', params),
  getFeePaymentDetail: (id) => apiClient.get(`/fee-payments/${id}/`),
  getOverduePayments: () => apiClient.get('/fee-payments/overdue/'),
  createFeePayment: (data) => apiClient.post('/fee-payments/', data),
  updateFeePayment: (id, data) => apiClient.put(`/fee-payments/${id}/`, data),

  // ============= Exams =============
  getExams: (params) => fetchPaginatedData('/exams/', params),
  getAllExams: (params) => fetchAllData('/exams/', params),
  getExamDetail: (id) => apiClient.get(`/exams/${id}/`),
  createExam: (data) => apiClient.post('/exams/', data),
  updateExam: (id, data) => apiClient.put(`/exams/${id}/`, data),
  publishResults: (id) => apiClient.post(`/exams/${id}/publish_results/`),

  // ============= Marks =============
  getMarks: (params) => fetchPaginatedData('/marks/', params),
  getAllMarks: (params) => fetchAllData('/marks/', params),
  getMarkDetail: (id) => apiClient.get(`/marks/${id}/`),
  createMark: (data) => apiClient.post('/marks/', data),
  updateMark: (id, data) => apiClient.put(`/marks/${id}/`, data),
  bulkUploadMarks: (data) => apiClient.post('/marks/bulk_upload/', data),

  // ============= Results =============
  getResults: (params) => fetchPaginatedData('/results/', params),
  getAllResults: (params) => fetchAllData('/results/', params),
  getResultDetail: (id) => apiClient.get(`/results/${id}/`),

  // ============= Transport Routes =============
  getTransportRoutes: (params) => fetchPaginatedData('/transport-routes/', params),
  getAllTransportRoutes: (params) => fetchAllData('/transport-routes/', params),
  getTransportRouteDetail: (id) => apiClient.get(`/transport-routes/${id}/`),
  createTransportRoute: (data) => apiClient.post('/transport-routes/', data),
  updateTransportRoute: (id, data) => apiClient.put(`/transport-routes/${id}/`, data),

  // ============= Vehicles =============
  getVehicles: (params) => fetchPaginatedData('/vehicles/', params),
  getAllVehicles: (params) => fetchAllData('/vehicles/', params),
  getVehicleDetail: (id) => apiClient.get(`/vehicles/${id}/`),
  createVehicle: (data) => apiClient.post('/vehicles/', data),
  updateVehicle: (id, data) => apiClient.put(`/vehicles/${id}/`, data),

  // ============= Homework =============
  getHomework: (params) => fetchPaginatedData('/homework/', params),
  getAllHomework: (params) => fetchAllData('/homework/', params),
  getHomeworkDetail: (id) => apiClient.get(`/homework/${id}/`),
  createHomework: (data) => apiClient.post('/homework/', data),
  updateHomework: (id, data) => apiClient.put(`/homework/${id}/`, data),

  // ============= Notifications =============
  getNotifications: (params) => fetchPaginatedData('/notifications/', params),
  getAllNotifications: (params) => fetchAllData('/notifications/', params),
  getNotificationDetail: (id) => apiClient.get(`/notifications/${id}/`),
  getUnreadNotifications: () => apiClient.get('/notifications/unread/'),
  createNotification: (data) => apiClient.post('/notifications/', data),
  updateNotification: (id, data) => apiClient.put(`/notifications/${id}/`, data),

  // ============= Library Books =============
  getLibraryBooks: (params) => fetchPaginatedData('/library-books/', params),
  getAllLibraryBooks: (params) => fetchAllData('/library-books/', params),
  getLibraryBookDetail: (id) => apiClient.get(`/library-books/${id}/`),
  createLibraryBook: (data) => apiClient.post('/library-books/', data),
  updateLibraryBook: (id, data) => apiClient.put(`/library-books/${id}/`, data),

  // ============= Complaints =============
  getComplaints: (params) => fetchPaginatedData('/complaints/', params),
  getAllComplaints: (params) => fetchAllData('/complaints/', params),
  getComplaintDetail: (id) => apiClient.get(`/complaints/${id}/`),
  createComplaint: (data) => apiClient.post('/complaints/', data),
  updateComplaint: (id, data) => apiClient.put(`/complaints/${id}/`, data),

  // ============= Certificates =============
  getCertificates: (params) => fetchPaginatedData('/certificates/', params),
  getAllCertificates: (params) => fetchAllData('/certificates/', params),
  getCertificateDetail: (id) => apiClient.get(`/certificates/${id}/`),
  createCertificate: (data) => apiClient.post('/certificates/', data),
  updateCertificate: (id, data) => apiClient.put(`/certificates/${id}/`, data),
};

// Export utility functions
export const apiUtils = {
  fetchPaginatedData,
  fetchAllData,
};

export default apiClient;
