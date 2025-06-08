import React, { useState } from 'react';
import { CreateUserI } from '../types/user';

interface CreateUserProps {
  onUserCreated: () => void;
}

const apiUrl = import.meta.env.VITE_API_URL;

const CreateUser: React.FC<CreateUserProps> = ({ onUserCreated }) => {
  const [formData, setFormData] = useState<CreateUserI>({
    id: 0,
    vorname: '',
    nachname: '',
    geburtsdatum: '',
    email: '',
    telefonnummer: '',
    strasse: '',
    hausnummer: '',
    plz: '',
    ort: '',
    land: ''
  });

  const [status, setStatus] = useState({
    message: '',
    isError: false,
    isLoading: false
  });

  const handleChange = (e: { target: { name: any; value: any; }; }) => {
    const { name, value } = e.target;

    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const validateForm = () => {
    if (!formData.vorname) return 'Vorname ist erforderlich';
    if (!formData.nachname) return 'Nachname ist erforderlich';
    if (!formData.geburtsdatum) return 'Geburtsdatum ist erforderlich';
    if (!formData.email) return 'E-Mail ist erforderlich';
    if (!formData.email.includes('@')) return 'Ungültige E-Mail-Adresse';
    if (!formData.telefonnummer) return 'Telefonnummer ist erforderlich';
    if (!formData.strasse) return 'Straße ist erforderlich';
    if (!formData.hausnummer) return 'Hausnummer ist erforderlich';
    if (!formData.plz) return 'PLZ ist erforderlich';
    if (!formData.ort) return 'Ort ist erforderlich';
    if (!formData.land) return 'Land ist erforderlich';
    return null;
  };

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    if (e) e.preventDefault();

    const validationError = validateForm();
    if (validationError) {
      setStatus({
        message: validationError,
        isError: true,
        isLoading: false
      });
      return;
    }

    setStatus({
      message: '',
      isError: false,
      isLoading: true
    });

    try {
      // Bereite die Daten für die API vor
      const userData = {
        ...formData,
      };

      const response = await fetch(`${apiUrl}/api/user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Fehler bei der Benutzererstellung');
      }

      // Erfolgreiche Antwort
      setStatus({
        message: result.message,
        isError: false,
        isLoading: false
      });

      // Formular zurücksetzen
      setFormData({
        id: 0,
        vorname: '',
        nachname: '',
        geburtsdatum: '',
        email: '',
        telefonnummer: '',
        strasse: '',
        hausnummer: '',
        plz: '',
        ort: '',
        land: ''
      });

      // Nutzer neu laden
      onUserCreated();

    } catch (error) {
      setStatus({
        message: "Problem to connect API",
        isError: true,
        isLoading: false
      });
    }
  };

  return (
    <div className="overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Neuer Nutzer</h2>
        <p className="mt-1 text-sm text-gray-600">Fügen Sie einen neuen Benutzer hinzu</p>
      </div>

      <div className="p-6">
        {status.message && (
          <div className={`mb-6 p-4 rounded-md ${status.isError ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="vorname" className="block text-sm font-medium text-gray-700 mb-1">Vorname</label>
              <input
                id="vorname"
                name="vorname"
                type="text"
                value={formData.vorname}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label htmlFor="nachname" className="block text-sm font-medium text-gray-700 mb-1">Nachname</label>
              <input
                id="nachname"
                name="nachname"
                type="text"
                value={formData.nachname}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label htmlFor="geburtsdatum" className="block text-sm font-medium text-gray-700 mb-1">Geburtsdatum</label>
            <input
              id="geburtsdatum"
              name="geburtsdatum"
              type="date"
              value={formData.geburtsdatum}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label htmlFor="telefonnummer" className="block text-sm font-medium text-gray-700 mb-1">Telefonnummer</label>
              <input
                id="telefonnummer"
                name="telefonnummer"
                type="tel"
                value={formData.telefonnummer}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="strasse" className="block text-sm font-medium text-gray-700 mb-1">Straße</label>
              <input
                id="strasse"
                name="strasse"
                type="text"
                value={formData.strasse}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label htmlFor="hausnummer" className="block text-sm font-medium text-gray-700 mb-1">Hausnummer</label>
              <input
                id="hausnummer"
                name="hausnummer"
                type="text"
                value={formData.hausnummer}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label htmlFor="plz" className="block text-sm font-medium text-gray-700 mb-1">PLZ</label>
              <input
                id="plz"
                name="plz"
                type="text"
                value={formData.plz}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label htmlFor="ort" className="block text-sm font-medium text-gray-700 mb-1">Ort</label>
              <input
                id="ort"
                name="ort"
                type="text"
                value={formData.ort}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label htmlFor="land" className="block text-sm font-medium text-gray-700 mb-1">Land</label>
              <input
                id="land"
                name="land"
                type="text"
                value={formData.land}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={status.isLoading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {status.isLoading ? 'Wird erstellt...' : 'Benutzer erstellen'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateUser;