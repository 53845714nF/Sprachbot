import React, { useState } from 'react';

const apiUrl = import.meta.env.VITE_API_URL;

const PdfStatistics: React.FC = () => {
  const [downloadLoading, setDownloadLoading] = useState<boolean>(false);
  const [viewLoading, setViewLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const handleDownloadPdf = async (): Promise<void> => {
    setDownloadLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${apiUrl}/api/download-statistics-pdf`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from Content-Disposition header or use default
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'personenstatistiken.pdf';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '');
        }
      }
      
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      setSuccess('PDF wurde erfolgreich heruntergeladen!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unbekannter Fehler';
      setError(`Fehler beim Herunterladen der PDF: ${errorMessage}`);
    } finally {
      setDownloadLoading(false);
    }
  };

  const handleViewPdf = async (): Promise<void> => {
    setViewLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${apiUrl}/api/view-statistics-pdf`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const newWindow = window.open(url, '_blank');
      
      if (!newWindow) {
        throw new Error('Pop-up wurde blockiert. Bitte erlauben Sie Pop-ups für diese Seite.');
      }
      
      // Clean up the URL after a delay
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
      }, 1000);
      
      setSuccess('PDF wurde in einem neuen Tab geöffnet!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unbekannter Fehler';
      setError(`Fehler beim Anzeigen der PDF: ${errorMessage}`);
    } finally {
      setViewLoading(false);
    }
  };

  const clearMessages = (): void => {
    setError('');
    setSuccess('');
  };

  return (
    <>
      <div className="px-4 py-3 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">Personenstatistiken PDF</h2>
          <p className="mt-1 text-sm text-gray-600">
            Erstellen Sie eine detaillierte PDF mit allen Personenstatistiken. 
            Sie können die PDF herunterladen oder direkt im Browser anzeigen.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row mb-6 mt-6 px-6 space-y-4 sm:space-y-0 sm:space-x-4">
          <button
            onClick={handleDownloadPdf}
            disabled={downloadLoading || viewLoading}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-3 rounded-md transition-colors duration-200 min-w-48"
          >
            {downloadLoading ? 'Wird heruntergeladen...' : 'PDF Herunterladen'}
          </button>
          
          <button
            onClick={handleViewPdf}
            disabled={downloadLoading || viewLoading}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white px-6 py-3 rounded-md transition-colors duration-200 min-w-48"
          >
            {viewLoading ? 'Wird geöffnet...' : 'PDF Anzeigen'}
          </button>
        </div>

        {/* Success Message */}
        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-5 h-5 bg-green-500 rounded-full flex">
                <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <span><strong>Erfolg:</strong> {success}</span>
            </div>
            <button
              onClick={clearMessages}
              className="text-green-700 hover:text-green-800 ml-4"
              >
              ×
            </button>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span><strong>Fehler:</strong> {error}</span>
            </div>
            <button
              onClick={clearMessages}
              className="text-red-700 hover:text-red-800 ml-4"
              >
              ×
            </button>
          </div>
        )}

        <div className="bg-gray-50 rounded-lg p-4 mt-6">
          <h3 className="font-medium text-gray-900 mb-2">Hinweise:</h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• <strong>Herunterladen:</strong> Lädt die PDF-Datei direkt auf Ihr Gerät herunter</li>
            <li>• <strong>Anzeigen:</strong> Öffnet die PDF in einem neuen Browser-Tab zur sofortigen Ansicht</li>
            <li>• Die PDF enthält aktuelle Statistiken basierend auf den vorhandenen Personendaten</li>
            <li>• Bei Problemen stellen Sie sicher, dass Pop-ups für diese Seite erlaubt sind</li>
          </ul>
        </div>
  </>
  );
};

export default PdfStatistics;