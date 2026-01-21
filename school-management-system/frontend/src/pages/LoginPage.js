import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Alert, Button, Input, Card, Loader } from '../components/UI';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // ✅ API-ONLY: Authenticate using backend API
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
      const response = await fetch(`${apiUrl}/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      
      if (!response.ok) {
        throw new Error('Invalid credentials');
      }
      
      const data = await response.json();
      
      // ✅ API-ONLY: Get user profile from API
      const profileResponse = await fetch(`${apiUrl}/users/profile/`, {
        headers: { 'Authorization': `Token ${data.token}` }
      });
      
      const userProfile = await profileResponse.json();
      login(data.token, userProfile);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">School Management System</h1>
        
        {error && <Alert type="error" message={error} className="mb-4" />}
        
        <form onSubmit={handleLogin} className="space-y-4">
          <Input
            label="Username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />
          <Button
            variant="primary"
            size="lg"
            type="submit"
            className="w-full"
          >
            Login
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default LoginPage;
