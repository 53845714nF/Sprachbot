import { useState, useEffect, useCallback } from 'react';
import UserTable from './components/UserTable';
import UserCountChart from './components/UserCountChart';
import CreateUser from './components/CreateUser';
import { User } from './types/user';
import SearchUser from './components/SearchUser';
import PdfStatistics from './components/PdfStatistics';
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
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="px-6 py-8 border-b border-gray-200">
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="mt-2 text-sm text-gray-600">Verwalten Sie Ihre Benutzer und Daten</p>
          </div>
          
          <div className="p-6 space-y-8">
            <div className="bg-white rounded-lg shadow-sm">
              <SearchUser />
            </div>
            
            <div className="bg-white rounded-lg shadow-sm">
              <UserCountChart users={users} />
            </div>
            
            <div className="bg-white rounded-lg shadow-sm">
              <UserTable users={users} onUpdate={handleUpdateUser}/>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm">
              <CreateUser onUserCreated={handleUpdateUser}/>
            </div>

            <div className="bg-white rounded-lg shadow-sm">
              <PdfStatistics />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
