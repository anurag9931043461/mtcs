import { useState, useEffect, useCallback } from 'react';
import { schoolApi, apiUtils } from '../services/apiEnhanced';

/**
 * Custom hook for fetching paginated data
 * @param {function} fetchFunction - API method to call
 * @param {object} params - Initial parameters
 * @returns {object} { data, loading, error, page, setPage, refetch, hasMore }
 */
export const usePaginatedFetch = (fetchFunction, params = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  const fetchData = useCallback(async (pageNum = 1) => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchFunction({ ...params, page: pageNum });
      setData(result.results || []);
      setHasMore(!!result.next);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, params]);

  useEffect(() => {
    fetchData(page);
  }, [page, fetchData]);

  return {
    data,
    loading,
    error,
    page,
    setPage,
    refetch: () => fetchData(page),
    hasMore,
  };
};

/**
 * Custom hook for fetching all data at once
 * @param {function} fetchFunction - API method to call
 * @param {object} params - Query parameters
 * @param {boolean} shouldFetch - Whether to fetch (default: true)
 * @returns {object} { data, loading, error, refetch }
 */
export const useAllDataFetch = (fetchFunction, params = {}, shouldFetch = true) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!shouldFetch) return;
    
    try {
      setLoading(true);
      setError(null);
      const result = await fetchFunction(params);
      setData(result);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, params, shouldFetch]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch: fetchData,
  };
};

/**
 * Custom hook for fetching a single item
 * @param {function} fetchFunction - API method to call
 * @param {string} id - Item ID
 * @param {boolean} shouldFetch - Whether to fetch
 * @returns {object} { data, loading, error, refetch }
 */
export const useItemFetch = (fetchFunction, id, shouldFetch = true) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!shouldFetch || !id) return;
    
    try {
      setLoading(true);
      setError(null);
      const result = await fetchFunction(id);
      setData(result);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, id, shouldFetch]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch: fetchData,
  };
};

/**
 * Custom hook for fetching multiple data sources in parallel
 * @param {array} fetchFunctions - Array of { method: function, params: object }
 * @returns {object} { data, loading, error, refetch }
 */
export const useMultipleFetch = (fetchFunctions = []) => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const promises = fetchFunctions.map(({ method, params = {} }) =>
        method(params)
      );
      
      const results = await Promise.all(promises);
      const resultData = {};
      
      fetchFunctions.forEach((config, index) => {
        resultData[config.key || `result${index}`] = results[index];
      });
      
      setData(resultData);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [fetchFunctions]);

  useEffect(() => {
    if (fetchFunctions.length > 0) {
      fetchData();
    }
  }, [fetchData, fetchFunctions]);

  return {
    data,
    loading,
    error,
    refetch: fetchData,
  };
};

/**
 * Example usage of custom hooks
 */

// Example 1: Using usePaginatedFetch
export function StudentListWithPagination() {
  const { data: students, page, setPage, loading, error, hasMore } = usePaginatedFetch(
    schoolApi.getStudents,
    { page_size: 20 }
  );

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      <ul>
        {students.map(student => (
          <li key={student.id}>{student.user?.first_name} {student.user?.last_name}</li>
        ))}
      </ul>

      <div>
        <button onClick={() => setPage(page - 1)} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={() => setPage(page + 1)} disabled={!hasMore}>
          Next
        </button>
      </div>
    </div>
  );
}

// Example 2: Using useAllDataFetch
export function AllStudentsList() {
  const { data: students, loading, error, refetch } = useAllDataFetch(
    schoolApi.getAllStudents
  );

  return (
    <div>
      <h2>All Students ({students.length})</h2>
      {loading && <p>Loading all students...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      <ul>
        {students.map(student => (
          <li key={student.id}>{student.user?.first_name} {student.user?.last_name}</li>
        ))}
      </ul>

      <button onClick={refetch}>Refresh</button>
    </div>
  );
}

// Example 3: Using useItemFetch
export function StudentDetail({ studentId }) {
  const { data: student, loading, error } = useItemFetch(
    schoolApi.getStudentDetail,
    studentId
  );

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;
  if (!student) return <p>No student found</p>;

  return (
    <div>
      <h2>{student.user?.first_name} {student.user?.last_name}</h2>
      <p>Roll Number: {student.roll_number}</p>
      <p>Gender: {student.gender}</p>
    </div>
  );
}

// Example 4: Using useMultipleFetch
export function DashboardWithMultipleData() {
  const { data, loading, error } = useMultipleFetch([
    { key: 'students', method: schoolApi.getAllStudents },
    { key: 'classes', method: schoolApi.getAllClasses },
    { key: 'subjects', method: schoolApi.getAllSubjects },
  ]);

  if (loading) return <p>Loading dashboard data...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <div>
        <h3>Total Students: {data.students?.length || 0}</h3>
      </div>
      <div>
        <h3>Total Classes: {data.classes?.length || 0}</h3>
      </div>
      <div>
        <h3>Total Subjects: {data.subjects?.length || 0}</h3>
      </div>
    </div>
  );
}

// Example 5: Filtered data fetching
export function FilteredStudents({ classId, gender }) {
  const { data: students, loading, error } = useAllDataFetch(
    schoolApi.getAllStudents,
    { 
      current_class: classId,
      gender: gender
    },
    !!classId // Only fetch if classId is provided
  );

  return (
    <div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      <p>Found {students.length} students</p>
      <ul>
        {students.map(student => (
          <li key={student.id}>{student.user?.first_name} {student.user?.last_name}</li>
        ))}
      </ul>
    </div>
  );
}
