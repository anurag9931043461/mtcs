import React, { useState, useEffect } from 'react';
import { schoolApi, apiUtils } from '../services/apiEnhanced';

/**
 * Example component showing how to fetch students data from API
 * This demonstrates different fetching patterns
 */
function DataFetchingExample() {
  const [students, setStudents] = useState([]);
  const [allStudents, setAllStudents] = useState([]);
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);

  // Pattern 1: Fetch paginated data (with pagination)
  useEffect(() => {
    fetchStudentsData();
  }, []);

  const fetchStudentsData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch first page of students
      const data = await schoolApi.getStudents({ page: 1, page_size: 10 });
      setStudents(data.results || []);
      console.log('Paginated students:', data);
    } catch (err) {
      setError('Failed to fetch students: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Pattern 2: Fetch ALL data (all pages at once)
  const handleFetchAllStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch all students from all pages
      const data = await schoolApi.getAllStudents();
      setAllStudents(data);
      console.log(`Fetched ${data.length} total students`);
    } catch (err) {
      setError('Failed to fetch all students: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Pattern 3: Fetch with filters
  const handleFetchFilteredStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch students filtered by class
      const data = await schoolApi.getStudents({ 
        current_class: selectedClass,
        page_size: 50 
      });
      setStudents(data.results || []);
      console.log('Filtered students:', data);
    } catch (err) {
      setError('Failed to fetch filtered students: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Pattern 4: Fetch related data
  const handleFetchStudentDetail = async (studentId) => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch specific student
      const student = await schoolApi.getStudentDetail(studentId);
      
      // Fetch student's attendance
      const attendance = await schoolApi.getStudentAttendance(studentId);
      
      // Fetch student's fee details
      const fees = await schoolApi.getStudentFees(studentId);
      
      console.log('Student Detail:', student);
      console.log('Student Attendance:', attendance);
      console.log('Student Fees:', fees);
    } catch (err) {
      setError('Failed to fetch student details: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Pattern 5: Fetch multiple data types at once
  const handleFetchAllData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch multiple resources in parallel
      const [studentsData, classesData, subjectsData] = await Promise.all([
        schoolApi.getAllStudents(),
        schoolApi.getAllClasses(),
        schoolApi.getAllSubjects(),
      ]);
      
      console.log('Students:', studentsData);
      console.log('Classes:', classesData);
      console.log('Subjects:', subjectsData);
    } catch (err) {
      setError('Failed to fetch data: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Pattern 6: Using generic utility function
  const handleFetchUsingUtility = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Using the generic utility function
      const data = await apiUtils.fetchAllData('/students/', { gender: 'MALE' });
      console.log('Male students:', data);
    } catch (err) {
      setError('Failed to fetch data: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>API Data Fetching Examples</h1>

      {error && (
        <div style={{ 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          padding: '10px', 
          marginBottom: '20px',
          borderRadius: '4px'
        }}>
          {error}
        </div>
      )}

      {loading && <div style={{ color: '#0c5460', marginBottom: '20px' }}>Loading...</div>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px', marginBottom: '20px' }}>
        
        {/* Button 1: Fetch Paginated Data */}
        <button 
          onClick={fetchStudentsData}
          style={{ padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          1. Fetch First Page Students
        </button>

        {/* Button 2: Fetch All Data */}
        <button 
          onClick={handleFetchAllStudents}
          style={{ padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          2. Fetch ALL Students
        </button>

        {/* Button 3: Fetch Filtered Data */}
        <button 
          onClick={handleFetchFilteredStudents}
          style={{ padding: '10px', backgroundColor: '#ffc107', color: 'black', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          3. Fetch Filtered Students
        </button>

        {/* Button 4: Fetch Related Data */}
        <button 
          onClick={() => students[0] && handleFetchStudentDetail(students[0].id)}
          style={{ padding: '10px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          4. Fetch Student Details & Related Data
        </button>

        {/* Button 5: Fetch All Types */}
        <button 
          onClick={handleFetchAllData}
          style={{ padding: '10px', backgroundColor: '#6f42c1', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          5. Fetch Multiple Data Types
        </button>

        {/* Button 6: Using Utility */}
        <button 
          onClick={handleFetchUsingUtility}
          style={{ padding: '10px', backgroundColor: '#e83e8c', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          6. Fetch Using Utility Function
        </button>
      </div>

      {/* Display Paginated Students */}
      {students.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h2>Paginated Students (First Page)</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #ddd' }}>
            <thead>
              <tr style={{ backgroundColor: '#f5f5f5' }}>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Roll Number</th>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Name</th>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Gender</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.id}>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{student.roll_number}</td>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                    {student.user?.first_name} {student.user?.last_name}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{student.gender}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Display All Students */}
      {allStudents.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <h2>All Students ({allStudents.length} total)</h2>
          <div style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #ddd' }}>
            <ul style={{ margin: '0', paddingLeft: '20px' }}>
              {allStudents.slice(0, 20).map(student => (
                <li key={student.id}>
                  {student.user?.first_name} {student.user?.last_name} - {student.roll_number}
                </li>
              ))}
              {allStudents.length > 20 && (
                <li>... and {allStudents.length - 20} more</li>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default DataFetchingExample;
