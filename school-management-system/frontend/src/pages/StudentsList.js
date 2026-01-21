import React, { useState, useEffect } from 'react';
import { Layout, Card } from '../components/Layout';
import { Button, Table, Input, Modal } from '../components/UI';
import { schoolApi } from '../services/api';
import { useAuth } from '../context/AuthContext';

const StudentsList = () => {
  const { user } = useAuth();
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    roll_number: '',
    admission_number: '',
    current_class: '',
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      // ✅ API-ONLY: Fetch all students from backend API
      const data = await schoolApi.getAllStudents();
      setStudents(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching students:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      // ✅ API-ONLY: Create student via backend API
      await schoolApi.createStudent(formData);
      setIsModalOpen(false);
      setFormData({ roll_number: '', admission_number: '', current_class: '' });
      // ✅ Refresh from API
      await fetchStudents();
    } catch (error) {
      console.error('Error adding student:', error);
    }
  };

  const columns = [
    { key: 'user', label: 'Name', render: (val) => `${val?.first_name} ${val?.last_name}` },
    { key: 'roll_number', label: 'Roll Number' },
    { key: 'admission_number', label: 'Admission Number' },
    { key: 'current_class', label: 'Class' },
  ];

  return (
    <Layout role={user?.role}>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Students</h1>
          <Button onClick={() => setIsModalOpen(true)}>Add Student</Button>
        </div>

        <Card>
          <Table columns={columns} data={students} loading={loading} />
        </Card>

        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add New Student">
          <form onSubmit={handleAddStudent} className="space-y-4">
            <Input
              label="Roll Number"
              value={formData.roll_number}
              onChange={(e) => setFormData({ ...formData, roll_number: e.target.value })}
              required
            />
            <Input
              label="Admission Number"
              value={formData.admission_number}
              onChange={(e) => setFormData({ ...formData, admission_number: e.target.value })}
              required
            />
            <Input
              label="Class"
              value={formData.current_class}
              onChange={(e) => setFormData({ ...formData, current_class: e.target.value })}
              required
            />
            <Button type="submit" className="w-full">Add Student</Button>
          </form>
        </Modal>
      </div>
    </Layout>
  );
};

export default StudentsList;
