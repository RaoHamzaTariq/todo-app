import { Reminder, CreateReminderRequest, UpdateReminderRequest } from '../types/reminder';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

class ReminderService {
  /**
   * Creates a new reminder
   * @param userId The ID of the user
   * @param reminderData The reminder data to create
   * @returns The created reminder
   */
  static async createReminder(userId: string, reminderData: CreateReminderRequest): Promise<Reminder> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/reminders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(reminderData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create reminder: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating reminder:', error);
      throw error;
    }
  }

  /**
   * Gets all reminders for a user
   * @param userId The ID of the user
   * @param limit Number of reminders to return (for pagination)
   * @param offset Number of reminders to skip (for pagination)
   * @returns Array of reminders
   */
  static async getReminders(userId: string, limit: number = 100, offset: number = 0): Promise<Reminder[]> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/users/${userId}/reminders?limit=${limit}&offset=${offset}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch reminders: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching reminders:', error);
      throw error;
    }
  }

  /**
   * Gets a specific reminder by ID
   * @param userId The ID of the user
   * @param reminderId The ID of the reminder to retrieve
   * @returns The requested reminder
   */
  static async getReminderById(userId: string, reminderId: number): Promise<Reminder> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/reminders/${reminderId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch reminder: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching reminder:', error);
      throw error;
    }
  }

  /**
   * Updates an existing reminder
   * @param userId The ID of the user
   * @param reminderId The ID of the reminder to update
   * @param reminderData The updated reminder data
   * @returns The updated reminder
   */
  static async updateReminder(
    userId: string,
    reminderId: number,
    reminderData: UpdateReminderRequest
  ): Promise<Reminder> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/reminders/${reminderId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(reminderData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update reminder: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating reminder:', error);
      throw error;
    }
  }

  /**
   * Deletes a reminder
   * @param userId The ID of the user
   * @param reminderId The ID of the reminder to delete
   */
  static async deleteReminder(userId: string, reminderId: number): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/reminders/${reminderId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to delete reminder: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error deleting reminder:', error);
      throw error;
    }
  }
}

export default ReminderService;