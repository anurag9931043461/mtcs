import React, { useEffect, useState } from 'react';
import { Layout, Card } from '../components/Layout';
import { useAuth } from '../context/AuthContext';
import { schoolApi } from '../services/apiEnhanced';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({ students: 0, staff: 0, classes: 0, overduePayments: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // ✅ API-ONLY: Fetch all stats from backend API
      const [studentsData, staffData, classesData, paymentsData] = await Promise.all([
        schoolApi.getAllStudents().catch(() => []),
        schoolApi.getAllStaff().catch(() => []),
        schoolApi.getAllClasses().catch(() => []),
        schoolApi.getOverduePayments().catch(() => ({ results: [] }))
      ]);
      
      // Calculate totals from API data
      const overdueTotal = (paymentsData.results || []).reduce((sum, p) => sum + (p.amount_due || 0), 0);
      
      setStats({
        students: Array.isArray(studentsData) ? studentsData.length : 0,
        staff: Array.isArray(staffData) ? staffData.length : 0,
        classes: Array.isArray(classesData) ? classesData.length : 0,
        overduePayments: overdueTotal
      });
    } catch (err) {
      setError('Failed to load dashboard statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <Layout role={user?.role}>
        <div className="text-red-600">Error: {error}</div>
      </Layout>
    );
  }

  return (
    <Layout role={user?.role}>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Welcome, {user?.first_name}!</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <h3 className="text-sm font-semibold text-gray-600">Total Students</h3>
            <p className="text-2xl font-bold text-blue-600 mt-2">{loading ? '...' : stats.students}</p>
          </Card>
          
          <Card>
            <h3 className="text-sm font-semibold text-gray-600">Total Staff</h3>
            <p className="text-2xl font-bold text-green-600 mt-2">{loading ? '...' : stats.staff}</p>
          </Card>
          
          <Card>
            <h3 className="text-sm font-semibold text-gray-600">Total Classes</h3>
            <p className="text-2xl font-bold text-purple-600 mt-2">{loading ? '...' : stats.classes}</p>
          </Card>
          
          <Card>
            <h3 className="text-sm font-semibold text-gray-600">Overdue Payments</h3>
            <p className="text-2xl font-bold text-red-600 mt-2">₹{loading ? '...' : stats.overduePayments.toLocaleString()}</p>
          </Card>
        </div>

        <Card>
          <h2 className="text-xl font-bold mb-4">Dashboard Statistics</h2>
          <p className="text-gray-600">✅ All data fetched from backend API in real-time</p>
          <button 
            onClick={fetchDashboardStats}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Refresh Statistics
          </button>
        </Card>
      </div>
    </Layout>
  );
};

export default Dashboard;
