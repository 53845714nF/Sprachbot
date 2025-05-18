import React from 'react';
import { User } from '../types/user';
import DeleteUser from './DeleteUser';

interface UserTableProps {
  users: User[];
  onUpdate: (userId: number) => void
}

const UserTable: React.FC<UserTableProps> = ({ users, onUpdate: onDelete }) => {
  return (
    <div className="max-w-full px-4 py-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Nutzer Daten</h2>

      <div className="overflow-x-auto rounded-lg shadow">
        <table className="min-w-full divide-y divide-blue-300"> {/* Farbe für die Trennlinien */}
          <thead className="bg-blue-100"> {/* Blauer Hintergrund für den Kopf */}
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Vorname</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Nachname</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Geburtstag</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Email</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Telefonnummer</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Straße</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Haus Nummer </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">PLZ</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Ort</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Land</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-blue-700 uppercase tracking-wider">Bearbeiten</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users.map((user, index) => (
              <tr
                key={user.id}
                className={index % 2 === 0 ? 'bg-white hover:bg-blue-50' : 'bg-gray-50 hover:bg-blue-50'}
              > {/* Blauer Hover-Effekt */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.vorname}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.nachname}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.geburtsdatum}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.kontakt.email}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.kontakt.telefonnummer}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.adresse.strasse}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.adresse.hausnummer}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.adresse.plz}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.adresse.ort}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">{user.adresse.land}</td>
                <td className="px-4 py-3 whitespace-nowrap text-sm"><DeleteUser userId={user.id} onUserDeleted={onDelete} /> </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserTable;