import React, { useState } from 'react';
import { SearchForm } from './components/SearchForm';
import { Plane } from 'lucide-react';
import type { SearchParams, ProcessedResults } from './types';

function App() {
  const [results, setResults] = useState<ProcessedResults | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (params: SearchParams) => {
    setLoading(true);
    try {
      // TODO: Implement actual API call to backend service
      // This is where we'll integrate with our scraping service
      console.log('Search params:', params);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock results for now
      setResults({
        bestOption: {
          site: 'Booking.com',
          price: 850,
          link: 'https://booking.com',
          description: 'Luxury Hotel in ' + params.destination,
          rating: 4.5,
          imageUrl: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&q=80'
        },
        allOptions: [],
        totalFound: 1
      });
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center space-x-3">
          <Plane className="h-8 w-8 text-blue-600" />
          <h1 className="text-2xl font-bold text-gray-900">AI Travel Assistant</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="space-y-8">
          <SearchForm onSearch={handleSearch} />

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Searching for the best options...</p>
            </div>
          )}

          {/* Results */}
          {results && !loading && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Best Option Found</h2>
              <div className="flex flex-col md:flex-row gap-6">
                <div className="md:w-1/3">
                  <img
                    src={results.bestOption.imageUrl}
                    alt={results.bestOption.description}
                    className="w-full h-48 object-cover rounded-lg"
                  />
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-lg font-medium">{results.bestOption.description}</h3>
                  <p className="text-gray-600 mt-2">Found on {results.bestOption.site}</p>
                  <div className="mt-4">
                    <span className="text-2xl font-bold text-blue-600">
                      ${results.bestOption.price}
                    </span>
                    <span className="text-gray-500 ml-2">per night</span>
                  </div>
                  {results.bestOption.rating && (
                    <div className="mt-2 flex items-center">
                      <span className="text-yellow-400">★</span>
                      <span className="ml-1">{results.bestOption.rating}/5</span>
                    </div>
                  )}
                  <a
                    href={results.bestOption.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-4 inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                  >
                    View Deal
                  </a>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;