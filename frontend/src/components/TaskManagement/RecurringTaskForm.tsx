import React, { useState } from 'react';

// Define TypeScript interfaces
interface RecurringTask {
  id?: number;
  title: string;
  description?: string;
  frequency: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  endDate?: string;
  active: boolean;
}

interface RecurringTaskFormProps {
  onSubmit: (taskData: RecurringTask) => Promise<void>;
  onCancel: () => void;
  recurringTask?: RecurringTask;
}

const RecurringTaskForm: React.FC<RecurringTaskFormProps> = ({ onSubmit, onCancel, recurringTask = null }) => {
  const [formData, setFormData] = useState<RecurringTask>({
    title: recurringTask?.title || '',
    description: recurringTask?.description || '',
    frequency: recurringTask?.frequency || 'weekly',
    interval: recurringTask?.interval || 1,
    endDate: recurringTask?.endDate || '',
    active: recurringTask?.active !== undefined ? recurringTask.active : true
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Handle input changes
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  /**
   * Validate form data
   */
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 255) {
      newErrors.title = 'Title must be 255 characters or less';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    if (!['daily', 'weekly', 'monthly', 'yearly'].includes(formData.frequency)) {
      newErrors.frequency = 'Invalid frequency';
    }

    if (formData.interval < 1) {
      newErrors.interval = 'Interval must be at least 1';
    }

    if (formData.endDate && new Date(formData.endDate) < new Date()) {
      newErrors.endDate = 'End date cannot be in the past';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsLoading(true);

    try {
      const taskData: RecurringTask = {
        ...formData,
        interval: parseInt(formData.interval.toString()),
        endDate: formData.endDate || undefined
      };

      await onSubmit(taskData);
    } catch (error) {
      console.error('Error submitting recurring task:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <form onSubmit={handleSubmit} className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-800 text-center">
          {recurringTask ? 'Edit Recurring Task' : 'Create Recurring Task'}
        </h2>

        <div className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.title ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Task title"
              disabled={isLoading}
            />
            {errors.title && <span className="text-red-500 text-sm">{errors.title}</span>}
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.description ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Task description"
              rows={3}
              disabled={isLoading}
            />
            {errors.description && <span className="text-red-500 text-sm">{errors.description}</span>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="frequency" className="block text-sm font-medium text-gray-700 mb-1">
                Frequency *
              </label>
              <select
                id="frequency"
                name="frequency"
                value={formData.frequency}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.frequency ? 'border-red-500' : 'border-gray-300'
                }`}
                disabled={isLoading}
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
              {errors.frequency && <span className="text-red-500 text-sm">{errors.frequency}</span>}
            </div>

            <div>
              <label htmlFor="interval" className="block text-sm font-medium text-gray-700 mb-1">
                Every * (occurrence)
              </label>
              <input
                type="number"
                id="interval"
                name="interval"
                min="1"
                value={formData.interval}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.interval ? 'border-red-500' : 'border-gray-300'
                }`}
                disabled={isLoading}
              />
              {errors.interval && <span className="text-red-500 text-sm">{errors.interval}</span>}
            </div>
          </div>

          <div>
            <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-1">
              End Date (optional)
            </label>
            <input
              type="date"
              id="endDate"
              name="endDate"
              value={formData.endDate}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.endDate ? 'border-red-500' : 'border-gray-300'
              }`}
              disabled={isLoading}
            />
            {errors.endDate && <span className="text-red-500 text-sm">{errors.endDate}</span>}
          </div>

          <div className="flex items-center justify-between">
            <label htmlFor="active" className="block text-sm font-medium text-gray-700">
              Active
            </label>
            <input
              type="checkbox"
              id="active"
              name="active"
              checked={formData.active}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              disabled={isLoading}
            />
          </div>
        </div>

        <div className="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            disabled={isLoading}
          >
            {isLoading ? 'Saving...' : (recurringTask ? 'Update' : 'Create')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default RecurringTaskForm;