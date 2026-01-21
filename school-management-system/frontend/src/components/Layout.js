import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="text-xl font-bold">School Management System</div>
        
        <div className="hidden md:flex items-center gap-6">
          <span className="text-sm">Welcome, {user?.first_name || 'User'}</span>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 hover:bg-blue-700 px-3 py-2 rounded"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>

        <button
          className="md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <Menu size={24} />
        </button>
      </div>

      {isMenuOpen && (
        <div className="md:hidden bg-blue-700 px-4 py-3 flex flex-col gap-2">
          <span className="text-sm">Welcome, {user?.first_name || 'User'}</span>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 hover:bg-blue-600 px-3 py-2 rounded w-full"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      )}
    </nav>
  );
};

export const Sidebar = ({ role }) => {
  const navigate = useNavigate();

  const menuItems = {
    SUPER_ADMIN: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'Users', path: '/users' },
      { label: 'Schools', path: '/schools' },
      { label: 'Academic Years', path: '/academic-years' },
      { label: 'Audit Logs', path: '/audit-logs' },
    ],
    ADMIN: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'Classes', path: '/classes' },
      { label: 'Students', path: '/students' },
      { label: 'Staff', path: '/staff' },
      { label: 'Fees', path: '/fees' },
      { label: 'Exams', path: '/exams' },
      { label: 'Transport', path: '/transport' },
      { label: 'Reports', path: '/reports' },
    ],
    TEACHER: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'My Classes', path: '/my-classes' },
      { label: 'Attendance', path: '/attendance' },
      { label: 'Marks', path: '/marks' },
      { label: 'Homework', path: '/homework' },
      { label: 'Class Diary', path: '/class-diary' },
    ],
    STUDENT: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'My Profile', path: '/profile' },
      { label: 'Attendance', path: '/attendance' },
      { label: 'Results', path: '/results' },
      { label: 'Homework', path: '/homework' },
      { label: 'Library', path: '/library' },
    ],
    PARENT: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'My Children', path: '/my-children' },
      { label: 'Fees', path: '/fees' },
      { label: 'Attendance', path: '/attendance' },
      { label: 'Results', path: '/results' },
    ],
    ACCOUNTANT: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'Fees', path: '/fees' },
      { label: 'Invoices', path: '/invoices' },
      { label: 'Payroll', path: '/payroll' },
      { label: 'Reports', path: '/reports' },
    ],
    TRANSPORT_MANAGER: [
      { label: 'Dashboard', path: '/dashboard' },
      { label: 'Routes', path: '/routes' },
      { label: 'Vehicles', path: '/vehicles' },
      { label: 'Drivers', path: '/drivers' },
      { label: 'Attendance', path: '/transport-attendance' },
    ],
  };

  const items = menuItems[role] || menuItems.STUDENT;

  return (
    <aside className="bg-gray-800 text-white w-64 min-h-screen p-4">
      <div className="mb-8">
        <h2 className="text-xl font-bold">Menu</h2>
      </div>
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item.path}>
            <button
              onClick={() => navigate(item.path)}
              className="w-full text-left px-4 py-2 rounded hover:bg-gray-700 transition"
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export const Layout = ({ children, role }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex">
        <Sidebar role={role} />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export const Card = ({ children, className = '' }) => (
  <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
    {children}
  </div>
);
