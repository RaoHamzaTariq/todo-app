export interface RecurringTask {
  id: number;
  userId: string;
  title: string;
  description?: string;
  frequency: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  endDate?: string;
  active: boolean;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface CreateRecurringTaskRequest {
  title: string;
  description?: string;
  frequency: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  endDate?: string;
  active: boolean;
}

export interface UpdateRecurringTaskRequest {
  title?: string;
  description?: string;
  frequency?: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval?: number;
  endDate?: string;
  active?: boolean;
}