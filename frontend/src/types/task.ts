export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  starred: boolean;
  created_at: string; // ISO string
  updated_at: string; // ISO string
  due_date?: string; // ISO string (optional)
  status: 'pending' | 'in-progress' | 'completed'; // Task status
  tags: string[]; // Array of tags
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high';
  starred?: boolean;
  due_date?: string; // ISO string
  status?: 'pending' | 'in-progress' | 'completed';
  tags?: string[];
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high';
  starred?: boolean;
  due_date?: string; // ISO string
  status?: 'pending' | 'in-progress' | 'completed';
  tags?: string[];
}

export interface TaskListResponse {
  tasks: Task[];
}

export interface SearchParams {
  status?: string;
  priority?: string;
  tag?: string;
  search?: string;
  sort_by?: 'created_at' | 'updated_at' | 'due_date' | 'priority';
  order?: 'asc' | 'desc';
  completed?: boolean;
}

export interface ApiError {
  detail: string;
}
