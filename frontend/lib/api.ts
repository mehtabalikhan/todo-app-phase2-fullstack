import {
  LoginResponse,
  RegisterResponse,
  TaskListResponse,
  TaskOperationResponse,
  Task,
  User,
  UserPreferences
} from './types';

// Base URL for the API - can be configured via environment variables
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

// Utility function to get auth headers
const getAuthHeaders = (token?: string) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

// Authentication API functions (mounted at /api/v1/)
export const authAPI = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${BASE_URL}/api/v1/login`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error(`Login failed: ${response.status}`);
    }

    return response.json();
  },

  async register(email: string, password: string, name?: string): Promise<RegisterResponse> {
    const response = await fetch(`${BASE_URL}/api/v1/register`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
      throw new Error(`Registration failed: ${response.status}`);
    }

    return response.json();
  },

  async logout(token: string): Promise<{ success: boolean }> {
    const response = await fetch(`${BASE_URL}/api/v1/logout`, {
      method: 'POST',
      headers: getAuthHeaders(token),
    });

    if (!response.ok) {
      throw new Error(`Logout failed: ${response.status}`);
    }

    return response.json();
  },

  async refreshToken(refreshToken: string): Promise<{ session: { accessToken: string } }> {
    const response = await fetch(`${BASE_URL}/api/v1/refresh`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ refreshToken }),
    });

    if (!response.ok) {
      throw new Error(`Token refresh failed: ${response.status}`);
    }

    return response.json();
  },
};

// Task API functions with user_id in URL
// These functions should be called from client-side components where session is available
export const taskAPI = {
  async getTasks(
    userId: string,
    token: string,
    filters?: { status?: string; priority?: string; search?: string; limit?: number; offset?: number }
  ): Promise<TaskListResponse> {
    // Build query string from filters
    const params = new URLSearchParams();
    if (filters?.status) params.append('status', filters.status);
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.search) params.append('search', filters.search);
    if (filters?.limit !== undefined) params.append('limit', filters.limit.toString());
    if (filters?.offset !== undefined) params.append('offset', filters.offset.toString());

    const queryString = params.toString();
    const url = `${BASE_URL}/api/${userId}/tasks${queryString ? '?' + queryString : ''}`;

    const response = await fetch(url, {
      headers: getAuthHeaders(token),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.status}`);
    }

    return response.json();
  },

  async createTask(userId: string, token: string, taskData: Partial<Task>): Promise<TaskOperationResponse> {
    const response = await fetch(`${BASE_URL}/api/${userId}/tasks`, {
      method: 'POST',
      headers: getAuthHeaders(token),
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.status}`);
    }

    return response.json();
  },

  async updateTask(userId: string, token: string, taskId: string, taskData: Partial<Task>): Promise<TaskOperationResponse> {
    const response = await fetch(`${BASE_URL}/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers: getAuthHeaders(token),
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.status}`);
    }

    return response.json();
  },

  async deleteTask(userId: string, token: string, taskId: string): Promise<{ success: boolean }> {
    const response = await fetch(`${BASE_URL}/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(token),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.status}`);
    }

    return response.json();
  },

  async toggleTaskCompletion(userId: string, token: string, taskId: string): Promise<TaskOperationResponse> {
    const response = await fetch(`${BASE_URL}/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers: getAuthHeaders(token),
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle task completion: ${response.status}`);
    }

    return response.json();
  },
};