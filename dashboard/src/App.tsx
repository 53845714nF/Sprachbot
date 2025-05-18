import { useState, useEffect, useCallback } from 'react';
import UserTable from './components/UserTable';
import UserCountChart from './components/UserCountChart';
import CreateUser from './components/CreateUser';
import { User } from './types/user';

const apiUrl = import.meta.env.VITE_API_URL;

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiUrl}/api/users`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setUsers(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleUpdateUser = useCallback(() => {
    fetchUsers();
  }, [fetchUsers]);

  if (loading) {
    return <div>Loading users...</div>;
  }

  if (error) {
    return <div>Error loading users: {error}</div>;
  }

 return (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-indigo-200 p-4">
    <div className="bg-white rounded-2xl shadow-xl p-8 w-full">
      <h1 className="text-3xl font-bold text-center text-indigo-700 mb-6">Admin Dashboard</h1>
      <div className="space-y-6">
        <UserCountChart users={users} />
        <UserTable users={users} onUpdate={handleUpdateUser}/>
        <CreateUser onUserCreated={handleUpdateUser}/>
      </div>
    </div>
  </div>
  );

}

export default App;
