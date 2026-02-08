export interface Reminder {
  id: number;
  userId: string;
  taskId: number;
  reminderDateTime: string; // ISO string format
  sent: boolean;
  channel: 'email' | 'push' | 'sms';
  createdAt: string; // ISO string
  updatedAt: string; // ISO string
}

export interface CreateReminderRequest {
  taskId: number;
  reminderDateTime: string; // ISO string
  channel: 'email' | 'push' | 'sms';
}

export interface UpdateReminderRequest {
  reminderDateTime?: string; // ISO string
  channel?: 'email' | 'push' | 'sms';
}