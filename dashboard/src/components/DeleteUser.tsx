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
        className={`bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${isDeleting ? 'opacity-50 cursor-not-allowed' : ''}`}
        disabled={isDeleting}
      >
        {isDeleting ? 'Löschen...' : 'Löschen'}
      </button>
      
      {errorMessage && (
        <p className="text-red-500 text-sm mt-2">{errorMessage}</p>
      )}
    </div>
  );
};

export default DeleteUser;