// User-related types
export interface User {
  id: string;
  email: string;
  name: string | null;
  createdAt: Date;
  updatedAt: Date;
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  notificationsEnabled: boolean;
  taskSortOrder: 'dueDate' | 'priority' | 'createdAt';
  dateFormat: string;
  weeklyDigest?: boolean;
}

// Session-related types
export interface Session {
  accessToken: string;
  refreshToken: string;
  expiresAt: Date;
  user: User;
}

// Task-related types
export interface Task {
  id: string;
  userId: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate: Date | null;
  createdAt: Date;
  updatedAt: Date;
  completedAt: Date | null;
}

// Filter-related types
export interface FilterState {
  status: 'all' | 'active' | 'completed';
  priority: 'all' | 'low' | 'medium' | 'high';
  searchTerm: string | null;
}

// API response types
export interface ApiResponse<T = any> {
  data?: T;
  error?: {
    message: string;
    code?: string;
  };
  success: boolean;
  status: number;
}

export interface LoginResponse {
  user: User;
  session: Session;
}

export interface RegisterResponse {
  user: User;
  session: Session;
}

export interface TaskListResponse {
  tasks: Task[];
  totalCount: number;
}

export interface TaskOperationResponse {
  task: Task;
  success: boolean;
}