import React, { useState } from 'react';

interface DeleteUserProps {
  userId: number;
  onUserDeleted?: (userId: number) => void;
}

const apiUrl = import.meta.env.VITE_API_URL;

const DeleteUser: React.FC<DeleteUserProps> = ({ userId, onUserDeleted }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleDelete = async () => {
    setIsDeleting(true);
    setErrorMessage(null);

    try {
      const response = await fetch(`${apiUrl}/api/user/${userId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data.message);
        if (onUserDeleted) {
          onUserDeleted(userId);
        }
      } else {
        setErrorMessage(`Fehler beim Löschen des Nutzers (Status: ${response.status})`);
      }
    } catch (error: any) {
      console.error('Fehler beim Senden der Anfrage:', error);
      setErrorMessage('Verbindungsfehler oder unerwarteter Fehler.');
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div>
      <button
        onClick={handleDelete}
        className={`inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200 ${isDeleting ? 'opacity-50 cursor-not-allowed' : ''}`}
        disabled={isDeleting}
      >
        {isDeleting ? 'Löschen...' : 'Löschen'}
      </button>
      
      {errorMessage && (
        <p className="mt-2 text-sm text-red-600">{errorMessage}</p>
      )}
    </div>
  );
};

export default DeleteUser;