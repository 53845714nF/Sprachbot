import React, { useState } from 'react';
import { User } from '../types/user';


const apiUrl = import.meta.env.VITE_API_URL;

interface SearchParams {
  vorname: string;
  nachname: string;
  telefonnummer: string;
  strasse: string;
  ort: string;
  land: string;
  plz: string;
}

interface Error {
  error: string;
}

type ApiResponse = User[] | Error;

const UserSearch: React.FC = () => {
  const [searchParams, setSearchParams] = useState<SearchParams>({
    vorname: '',
    nachname: '',
    telefonnummer: '',
    strasse: '',
    ort: '',
    land: '',
    plz: ''
  });
  
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [hasSearched, setHasSearched] = useState<boolean>(false);

  const handleInputChange = (field: keyof SearchParams, value: string): void => {
    setSearchParams((prev: any) => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSearch = async (): Promise<void> => {
    setLoading(true);
    setError('');
    setHasSearched(true);

    // Build query parameters
    const queryParams = new URLSearchParams();
    Object.entries(searchParams).forEach(([key, value]) => {
      if (typeof value === 'string' && value.trim()) {
        queryParams.append(key, value.trim());
      }
    });

    try {
      const response = await fetch(`${apiUrl}/api/search?${queryParams.toString()}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: ApiResponse = await response.json();
      
      if ('error' in data) {
        setError(data.error);
        setUsers([]);
      } else {
        setUsers(data);
        setError('');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unbekannter Fehler';
      setError(`Fehler bei der Suche: ${errorMessage}`);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = (): void => {
    setSearchParams({
      vorname: '',
      nachname: '',
      telefonnummer: '',
      strasse: '',
      ort: '',
      land: '',
      plz: ''
    });
    setUsers([]);
    setError('');
    setHasSearched(false);
  };

  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'Nicht angegeben';
    try {
      return new Date(dateString).toLocaleDateString('de-DE');
    } catch {
      return dateString;
    }
  };

  const renderInputField = (
    label: string,
    field: keyof SearchParams,
    placeholder: string,
    colSpan?: string
  ) => (
    <div className={colSpan || ''}>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <input
        type="text"
        value={searchParams[field]}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => 
          handleInputChange(field, e.target.value)
        }
        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder={placeholder}
      />
    </div>
  );

  const renderUserCard = (user: User) => (
    <div key={user.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">

      <div className="flex items-center gap-3 mb-3">
        <div>
          <h3 className="font-semibold text-gray-900">
            {user.vorname} {user.nachname}
          </h3>
          <p className="text-sm text-gray-500">ID: {user.id}</p>
        </div>
      </div>

      <div className="space-y-2 text-sm">
        {/* Geburtsdatum */}
        <div className="flex items-center gap-2 text-gray-600">
          <span>Geburtsdatum: {formatDate(user.geburtsdatum)}</span>
        </div>

        {user.kontakt && (
          <div className="space-y-1">
            {user.kontakt.email && (
              <div className="flex items-center gap-2 text-gray-600">
                <span>{user.kontakt.email}</span>
              </div>
            )}
            {user.kontakt.telefonnummer && (
              <div className="flex items-center gap-2 text-gray-600">
                <span>{user.kontakt.telefonnummer}</span>
              </div>
            )}
          </div>
        )}

        {user.adresse && (
          <div className="flex items-start gap-2 text-gray-600">
            <div>
              <div>{user.adresse.strasse} {user.adresse.hausnummer}</div>
              <div>{user.adresse.plz} {user.adresse.ort}</div>
              {user.adresse.land && <div>{user.adresse.land}</div>}
            </div>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Benutzersuche</h1>
        <p className="text-gray-600">Suchen Sie nach Benutzern anhand verschiedener Kriterien</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {renderInputField('Vorname', 'vorname', 'Max')}
          {renderInputField('Nachname', 'nachname', 'Mustermann')}
          {renderInputField('Telefonnummer', 'telefonnummer', '+49 123 456789')}
          {renderInputField('Straße', 'strasse', 'Musterstraße')}
          {renderInputField('Ort', 'ort', 'Berlin')}
          {renderInputField('PLZ', 'plz', '10115')}
          {renderInputField('Land', 'land', 'Deutschland', 'md:col-span-2 lg:col-span-1')}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={handleSearch}
            disabled={loading}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-md transition-colors duration-200"
          >
            {loading ? 'Suche läuft...' : 'Suchen'}
          </button>
          
          <button
            onClick={handleReset}
            className="flex items-center gap-2 bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-md transition-colors duration-200"
          >
            Zurücksetzen
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <strong>Fehler:</strong> {error}
        </div>
      )}

      {/* Results */}
      {hasSearched && !loading && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Suchergebnisse ({users.length})
          </h2>
          
          {users.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>Keine Benutzer gefunden.</p>
              <p className="text-sm">Versuchen Sie es mit anderen Suchkriterien.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {users.map(renderUserCard)}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default UserSearch;