import React from 'react';
import { User } from '../types/user';
import DeleteUser from './DeleteUser';

interface UserTableProps {
  users: User[];
  onUpdate: (userId: number) => void
}

const UserTable: React.FC<UserTableProps> = ({ users, onUpdate: onDelete }) => {
  return (
    <>
      <div className="px-4 py-3 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Nutzer Daten</h2>
        <p className="mt-1 text-sm text-gray-600">Hier können Sie alle Nutzerdaten ansehen</p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vorname</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nachname</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Geburtstag</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefon</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Straße</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nr.</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">PLZ</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ort</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Land</th>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aktionen</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users.map((user, index) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.vorname}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.nachname}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.geburtsdatum}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.kontakt.email}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.kontakt.telefonnummer}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.adresse.strasse}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.adresse.hausnummer}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.adresse.plz}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.adresse.ort}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">{user.adresse.land}</td>
                <td className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">
                  <DeleteUser userId={user.id} onUserDeleted={onDelete} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default UserTable;