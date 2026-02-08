import { Task, CreateTaskInput, UpdateTaskInput, SearchParams } from '../types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

class TaskService {
  /**
   * Creates a new task
   * @param userId The ID of the user
   * @param taskData The task data to create
   * @returns The created task
   */
  static async createTask(userId: string, taskData: CreateTaskInput): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create task: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  /**
   * Gets all tasks for a user
   * @param userId The ID of the user
   * @param params Optional search and filter parameters
   * @returns Array of tasks
   */
  static async getTasks(userId: string, params?: SearchParams): Promise<Task[]> {
    try {
      // Build query string from params
      const queryParams = new URLSearchParams();

      if (params) {
        if (params.status) queryParams.append('status', params.status);
        if (params.priority) queryParams.append('priority', params.priority);
        if (params.tag) queryParams.append('tag', params.tag);
        if (params.search) queryParams.append('q', params.search);
        if (params.completed !== undefined) queryParams.append('completed', params.completed.toString());
        if (params.sort_by) queryParams.append('sort_by', params.sort_by);
        if (params.order) queryParams.append('order', params.order);
      }

      const queryString = queryParams.toString();
      const url = queryString
        ? `${API_BASE_URL}/users/${userId}/tasks?${queryString}`
        : `${API_BASE_URL}/users/${userId}/tasks`;

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  /**
   * Gets a specific task by ID
   * @param userId The ID of the user
   * @param taskId The ID of the task to retrieve
   * @returns The requested task
   */
  static async getTaskById(userId: string, taskId: number): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch task: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching task:', error);
      throw error;
    }
  }

  /**
   * Updates an existing task
   * @param userId The ID of the user
   * @param taskId The ID of the task to update
   * @param taskData The updated task data
   * @returns The updated task
   */
  static async updateTask(userId: string, taskId: number, taskData: UpdateTaskInput): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update task: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  /**
   * Deletes a task
   * @param userId The ID of the user
   * @param taskId The ID of the task to delete
   */
  static async deleteTask(userId: string, taskId: number): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }

  /**
   * Toggles the completion status of a task
   * @param userId The ID of the user
   * @param taskId The ID of the task to toggle
   * @returns The updated task
   */
  static async toggleTaskCompletion(userId: string, taskId: number): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/${taskId}/complete`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to toggle task completion: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  }

  /**
   * Searches tasks with filters and sorting
   * @param userId The ID of the user
   * @param searchQuery The search query string
   * @param params Optional search and filter parameters
   * @returns Array of matching tasks
   */
  static async searchTasks(userId: string, searchQuery: string, params?: SearchParams): Promise<Task[]> {
    try {
      // Build query string from search and params
      const queryParams = new URLSearchParams();
      queryParams.append('q', searchQuery);

      if (params) {
        if (params.status) queryParams.append('status', params.status);
        if (params.priority) queryParams.append('priority', params.priority);
        if (params.tag) queryParams.append('tag', params.tag);
        if (params.completed !== undefined) queryParams.append('completed', params.completed.toString());
        if (params.sort_by) queryParams.append('sort_by', params.sort_by);
        if (params.order) queryParams.append('order', params.order);
      }

      const queryString = queryParams.toString();
      const url = `${API_BASE_URL}/users/${userId}/tasks/search?${queryString}`;

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to search tasks: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error searching tasks:', error);
      throw error;
    }
  }
}

export default TaskService;