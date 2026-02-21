const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ApiRequestOptions extends RequestInit {
  requiresAuth?: boolean;
}

async function apiRequest<T>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<T> {
  const { requiresAuth = false, ...fetchOptions } = options;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (fetchOptions.headers) {
    Object.assign(headers, fetchOptions.headers);
  }

  if (requiresAuth) {
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'An error occurred');
  }

  return response.json();
}

export const authApi = {
  register: (data: { email: string; password: string; full_name: string }) =>
    apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  login: (data: { email: string; password: string }) =>
    apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

export const workspaceApi = {
  create: (data: { name: string; description?: string }) =>
    apiRequest('/workspaces', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: true,
    }),

  getAll: () =>
    apiRequest('/workspaces', {
      method: 'GET',
      requiresAuth: true,
    }),

  getById: (id: string) =>
    apiRequest(`/workspaces/${id}`, {
      method: 'GET',
      requiresAuth: true,
    }),

  update: (id: string, data: { name?: string; description?: string }) =>
    apiRequest(`/workspaces/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
      requiresAuth: true,
    }),

  delete: (id: string) =>
    apiRequest(`/workspaces/${id}`, {
      method: 'DELETE',
      requiresAuth: true,
    }),
};

export const paperApi = {
  search: (query: string, limit: number = 10) =>
    apiRequest('/papers/search', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
      requiresAuth: true,
    }),

  import: (workspaceId: string, paperId: string) =>
    apiRequest('/papers/import', {
      method: 'POST',
      body: JSON.stringify({ workspace_id: workspaceId, paper_id: paperId }),
      requiresAuth: true,
    }),

  getWorkspacePapers: (workspaceId: string) =>
    apiRequest(`/papers/workspace/${workspaceId}`, {
      method: 'GET',
      requiresAuth: true,
    }),

  upload: async (file: File, title: string, authors: string) => {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
      `${API_BASE_URL}/papers/upload?title=${encodeURIComponent(title)}&authors=${encodeURIComponent(authors)}`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      }
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(error.detail || 'Upload failed');
    }

    return response.json();
  },

  removeFromWorkspace: (workspaceId: string, paperId: string) =>
    apiRequest(`/papers/workspace/${workspaceId}/paper/${paperId}`, {
      method: 'DELETE',
      requiresAuth: true,
    }),
};

export const chatApi = {
  createConversation: (workspaceId: string, title?: string) =>
    apiRequest('/chat/conversations', {
      method: 'POST',
      body: JSON.stringify({ workspace_id: workspaceId, title }),
      requiresAuth: true,
    }),

  getWorkspaceConversations: (workspaceId: string) =>
    apiRequest(`/chat/conversations/workspace/${workspaceId}`, {
      method: 'GET',
      requiresAuth: true,
    }),

  getMessages: (conversationId: string) =>
    apiRequest(`/chat/conversations/${conversationId}/messages`, {
      method: 'GET',
      requiresAuth: true,
    }),

  sendMessage: (workspaceId: string, conversationId: string, message: string) =>
    apiRequest('/chat', {
      method: 'POST',
      body: JSON.stringify({ workspace_id: workspaceId, conversation_id: conversationId, message }),
      requiresAuth: true,
    }),

  deleteConversation: (conversationId: string) =>
    apiRequest(`/chat/conversations/${conversationId}`, {
      method: 'DELETE',
      requiresAuth: true,
    }),
};
