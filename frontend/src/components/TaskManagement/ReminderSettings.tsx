import React, { useState, useEffect } from 'react';
import { Reminder, CreateReminderRequest, UpdateReminderRequest } from '../../types/reminder';
import ReminderService from '../../services/reminderService';
import './ReminderSettings.css';

interface ReminderSettingsProps {
  userId: string;
  taskId?: number;
  onReminderAdded?: (reminder: Reminder) => void;
  onReminderUpdated?: (reminder: Reminder) => void;
  onReminderDeleted?: (reminderId: number) => void;
}

const ReminderSettings: React.FC<ReminderSettingsProps> = ({
  userId,
  taskId,
  onReminderAdded,
  onReminderUpdated,
  onReminderDeleted
}) => {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    reminderDateTime: '',
    channel: 'email',
    taskId: taskId || 0
  });

  // Fetch existing reminders
  useEffect(() => {
    const fetchReminders = async () => {
      try {
        setIsLoading(true);
        const userReminders = await ReminderService.getReminders(userId);

        // Filter reminders by taskId if provided
        const filteredReminders = taskId
          ? userReminders.filter(reminder => reminder.taskId === taskId)
          : userReminders;

        setReminders(filteredReminders);
        setError(null);
      } catch (err) {
        setError('Failed to load reminders');
        console.error('Error fetching reminders:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchReminders();
  }, [userId, taskId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'taskId' ? parseInt(value, 10) : value
    }));
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (!formData.reminderDateTime) {
        setError('Reminder date and time are required');
        return;
      }

      // Use taskId from props if not provided in form
      const finalTaskId = formData.taskId || taskId;
      if (!finalTaskId) {
        setError('Task ID is required');
        return;
      }

      const newReminderData: CreateReminderRequest = {
        taskId: finalTaskId,
        reminderDateTime: new Date(formData.reminderDateTime).toISOString(),
        channel: formData.channel as 'email' | 'push' | 'sms'
      };

      const newReminder = await ReminderService.createReminder(userId, newReminderData);
      setReminders([...reminders, newReminder]);

      if (onReminderAdded) {
        onReminderAdded(newReminder);
      }

      // Reset form
      setFormData({
        reminderDateTime: '',
        channel: 'email',
        taskId: taskId || 0
      });
      setShowForm(false);
      setError(null);
    } catch (err) {
      setError('Failed to create reminder');
      console.error('Error creating reminder:', err);
    }
  };

  const handleDelete = async (reminderId: number) => {
    try {
      await ReminderService.deleteReminder(userId, reminderId);
      setReminders(reminders.filter(r => r.id !== reminderId));

      if (onReminderDeleted) {
        onReminderDeleted(reminderId);
      }
    } catch (err) {
      setError('Failed to delete reminder');
      console.error('Error deleting reminder:', err);
    }
  };

  const handleUpdate = async (reminderId: number, updatedData: UpdateReminderRequest) => {
    try {
      const updatedReminder = await ReminderService.updateReminder(userId, reminderId, updatedData);
      setReminders(reminders.map(r => r.id === reminderId ? updatedReminder : r));

      if (onReminderUpdated) {
        onReminderUpdated(updatedReminder);
      }
    } catch (err) {
      setError('Failed to update reminder');
      console.error('Error updating reminder:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="reminder-settings-loading">
        <div className="spinner"></div>
        <p>Loading reminders...</p>
      </div>
    );
  }

  return (
    <div className="reminder-settings">
      <div className="reminder-settings-header">
        <h2>Reminder Settings</h2>
        <button
          className="add-reminder-btn"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Add Reminder'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {showForm && (
        <form className="reminder-form" onSubmit={handleFormSubmit}>
          {taskId ? (
            <input
              type="hidden"
              name="taskId"
              value={taskId}
            />
          ) : (
            <div className="form-group">
              <label htmlFor="taskId">Task ID:</label>
              <input
                type="number"
                id="taskId"
                name="taskId"
                value={formData.taskId}
                onChange={handleInputChange}
                required
                min="1"
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="reminderDateTime">Date & Time:</label>
            <input
              type="datetime-local"
              id="reminderDateTime"
              name="reminderDateTime"
              value={formData.reminderDateTime}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="channel">Channel:</label>
            <select
              id="channel"
              name="channel"
              value={formData.channel}
              onChange={handleInputChange}
            >
              <option value="email">Email</option>
              <option value="push">Push Notification</option>
              <option value="sms">SMS</option>
            </select>
          </div>

          <button type="submit" className="submit-btn">
            Set Reminder
          </button>
        </form>
      )}

      <div className="reminders-list">
        <h3>Scheduled Reminders ({reminders.length})</h3>
        {reminders.length === 0 ? (
          <p className="no-reminders">No reminders scheduled</p>
        ) : (
          <ul className="reminder-list">
            {reminders.map(reminder => (
              <li key={reminder.id} className="reminder-item">
                <div className="reminder-info">
                  <div className="reminder-date">
                    {new Date(reminder.reminderDateTime).toLocaleString()}
                  </div>
                  <div className="reminder-channel">
                    Channel: {reminder.channel}
                  </div>
                  <div className={`reminder-status ${reminder.sent ? 'sent' : 'pending'}`}>
                    Status: {reminder.sent ? 'Sent' : 'Pending'}
                  </div>
                </div>
                <div className="reminder-actions">
                  {!reminder.sent && (
                    <button
                      className="update-btn"
                      onClick={() => handleUpdate(reminder.id, {
                        ...reminder,
                        channel: reminder.channel === 'email' ? 'push' : 'email' // Toggle channel as an example
                      })}
                    >
                      Update
                    </button>
                  )}
                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(reminder.id)}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ReminderSettings;