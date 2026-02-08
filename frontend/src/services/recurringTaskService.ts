import { RecurringTask } from '../types/recurringTask';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Service class for handling recurring task API operations
 */
class RecurringTaskService {
  /**
   * Creates a new recurring task
   * @param userId - The ID of the user creating the task
   * @param taskData - The recurring task data
   * @returns The created recurring task
   */
  static async createRecurringTask(userId: string, taskData: Omit<RecurringTask, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<RecurringTask> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/recurring`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`, // Assuming JWT token is stored
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create recurring task: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating recurring task:', error);
      throw error;
    }
  }

  /**
   * Fetches all recurring tasks for a user
   * @param userId - The ID of the user
   * @param limit - Maximum number of tasks to return (for pagination)
   * @param offset - Number of tasks to skip (for pagination)
   * @returns Array of recurring tasks
   */
  static async getRecurringTasks(userId: string, limit: number = 100, offset: number = 0): Promise<RecurringTask[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/recurring?limit=${limit}&offset=${offset}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`, // Assuming JWT token is stored
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch recurring tasks: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching recurring tasks:', error);
      throw error;
    }
  }

  /**
   * Fetches a specific recurring task by ID
   * @param userId - The ID of the user
   * @param taskId - The ID of the recurring task
   * @returns The recurring task
   */
  static async getRecurringTaskById(userId: string, taskId: number): Promise<RecurringTask> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/recurring/${taskId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`, // Assuming JWT token is stored
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch recurring task: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching recurring task:', error);
      throw error;
    }
  }

  /**
   * Updates an existing recurring task
   * @param userId - The ID of the user
   * @param taskId - The ID of the recurring task to update
   * @param taskData - The updated recurring task data
   * @returns The updated recurring task
   */
  static async updateRecurringTask(userId: string, taskId: number, taskData: Partial<Omit<RecurringTask, 'id' | 'userId' | 'createdAt' | 'updatedAt'>>): Promise<RecurringTask> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/recurring/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`, // Assuming JWT token is stored
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update recurring task: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating recurring task:', error);
      throw error;
    }
  }

  /**
   * Deletes (deactivates) a recurring task
   * @param userId - The ID of the user
   * @param taskId - The ID of the recurring task to delete
   */
  static async deleteRecurringTask(userId: string, taskId: number): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/tasks/recurring/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`, // Assuming JWT token is stored
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to delete recurring task: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error deleting recurring task:', error);
      throw error;
    }
  }
}

export default RecurringTaskService;