import { useState } from 'react';
import { Search, Plus, X, Loader } from 'lucide-react';
import { paperApi } from '../services/api';

interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  publication_date: string | null;
  pdf_url: string | null;
  arxiv_id: string | null;
}

interface Props {
  workspaceId: string;
  onClose: () => void;
  onPaperAdded: () => void;
}

export default function PaperSearch({ workspaceId, onClose, onPaperAdded }: Props) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Paper[]>([]);
  const [searching, setSearching] = useState(false);
  const [importing, setImporting] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearching(true);
    try {
      const results: any = await paperApi.search(searchQuery, 10);
      setSearchResults(results);
    } catch (error) {
      console.error('Search failed:', error);
      alert('Failed to search papers. Please try again.');
    } finally {
      setSearching(false);
    }
  };

  const handleImport = async (paperId: string) => {
    setImporting(paperId);
    try {
      await paperApi.import(workspaceId, paperId);
      onPaperAdded();
      alert('Paper imported successfully!');
    } catch (error: any) {
      console.error('Import failed:', error);
      if (error.message.includes('already in workspace')) {
        alert('This paper is already in your workspace.');
      } else {
        alert('Failed to import paper. Please try again.');
      }
    } finally {
      setImporting(null);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-900">Search Research Papers</h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by keywords, topics, or authors..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <button
              type="submit"
              disabled={searching}
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {searching ? <Loader className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
              Search
            </button>
          </form>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {searchResults.length === 0 && !searching && (
            <div className="text-center py-12">
              <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">Search for research papers from arXiv</p>
            </div>
          )}

          {searching && (
            <div className="text-center py-12">
              <Loader className="w-12 h-12 text-indigo-600 mx-auto mb-4 animate-spin" />
              <p className="text-gray-600">Searching papers...</p>
            </div>
          )}

          <div className="space-y-4">
            {searchResults.map((paper) => (
              <div
                key={paper.id}
                className="bg-gray-50 rounded-lg border border-gray-200 p-4 hover:border-indigo-300 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-2">{paper.title}</h4>
                    <p className="text-sm text-gray-600 mb-2">
                      {paper.authors.join(', ')}
                    </p>
                    <p className="text-sm text-gray-700 line-clamp-3 mb-2">
                      {paper.abstract}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      {paper.publication_date && (
                        <span>{new Date(paper.publication_date).toLocaleDateString()}</span>
                      )}
                      {paper.arxiv_id && <span>arXiv: {paper.arxiv_id}</span>}
                    </div>
                  </div>
                  <button
                    onClick={() => handleImport(paper.id)}
                    disabled={importing === paper.id}
                    className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                  >
                    {importing === paper.id ? (
                      <Loader className="w-4 h-4 animate-spin" />
                    ) : (
                      <Plus className="w-4 h-4" />
                    )}
                    Import
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
