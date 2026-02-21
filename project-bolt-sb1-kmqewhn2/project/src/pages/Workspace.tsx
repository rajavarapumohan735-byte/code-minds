import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, MessageSquare, FileText, X } from 'lucide-react';
import { workspaceApi, paperApi } from '../services/api';
import PaperSearch from '../components/PaperSearch';
import ChatInterface from '../components/ChatInterface';

interface Workspace {
  id: string;
  name: string;
  description: string;
}

interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  publication_date: string | null;
  pdf_url: string | null;
  arxiv_id: string | null;
}

export default function Workspace() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [activeTab, setActiveTab] = useState<'papers' | 'chat'>('papers');
  const [showSearchModal, setShowSearchModal] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadWorkspace();
      loadPapers();
    }
  }, [id]);

  const loadWorkspace = async () => {
    try {
      const data: any = await workspaceApi.getById(id!);
      setWorkspace(data);
    } catch (error) {
      console.error('Failed to load workspace:', error);
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const loadPapers = async () => {
    try {
      const data: any = await paperApi.getWorkspacePapers(id!);
      setPapers(data);
    } catch (error) {
      console.error('Failed to load papers:', error);
    }
  };

  const handleRemovePaper = async (paperId: string) => {
    if (!confirm('Remove this paper from workspace?')) return;

    try {
      await paperApi.removeFromWorkspace(id!, paperId);
      loadPapers();
    } catch (error) {
      console.error('Failed to remove paper:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">{workspace?.name}</h1>
              {workspace?.description && (
                <p className="text-sm text-gray-600 mt-1">{workspace.description}</p>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('papers')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'papers'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
            }`}
          >
            <FileText className="w-5 h-5" />
            Papers ({papers.length})
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'chat'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
            AI Chat
          </button>
        </div>

        {activeTab === 'papers' ? (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Research Papers</h2>
              <button
                onClick={() => setShowSearchModal(true)}
                className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                <Search className="w-5 h-5" />
                Search Papers
              </button>
            </div>

            {papers.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No papers yet</h3>
                <p className="text-gray-600 mb-4">
                  Search and import research papers to get started
                </p>
                <button
                  onClick={() => setShowSearchModal(true)}
                  className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
                >
                  <Search className="w-5 h-5" />
                  Search Papers
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {papers.map((paper) => (
                  <div
                    key={paper.id}
                    className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {paper.title}
                        </h3>
                        <p className="text-sm text-gray-600 mb-2">
                          {paper.authors.join(', ')}
                        </p>
                        <p className="text-sm text-gray-700 line-clamp-3 mb-3">
                          {paper.abstract}
                        </p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          {paper.publication_date && (
                            <span>{new Date(paper.publication_date).toLocaleDateString()}</span>
                          )}
                          {paper.arxiv_id && <span>arXiv: {paper.arxiv_id}</span>}
                          {paper.pdf_url && (
                            <a
                              href={paper.pdf_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-indigo-600 hover:text-indigo-700"
                            >
                              View PDF
                            </a>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={() => handleRemovePaper(paper.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <ChatInterface workspaceId={id!} />
        )}
      </div>

      {showSearchModal && (
        <PaperSearch
          workspaceId={id!}
          onClose={() => setShowSearchModal(false)}
          onPaperAdded={loadPapers}
        />
      )}
    </div>
  );
}
