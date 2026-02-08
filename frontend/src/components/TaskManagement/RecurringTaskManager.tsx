import React, { useState, useEffect } from 'react';
import RecurringTaskService from '../../services/recurringTaskService';
import { RecurringTask } from '../../types/recurringTask';
import RecurringTaskForm from './RecurringTaskForm';

interface RecurringTaskManagerProps {
  userId: string;
}

const RecurringTaskManager: React.FC<RecurringTaskManagerProps> = ({ userId }) => {
  const [recurringTasks, setRecurringTasks] = useState<RecurringTask[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<RecurringTask | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRecurringTasks();
  }, [userId]);

  const fetchRecurringTasks = async () => {
    try {
      setLoading(true);
      const tasks = await RecurringTaskService.getRecurringTasks(userId);
      setRecurringTasks(tasks);
      setError(null);
    } catch (err) {
      setError('Failed to load recurring tasks');
      console.error('Error fetching recurring tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSubmit = async (taskData: Omit<RecurringTask, 'id' | 'userId' | 'createdAt' | 'updatedAt'>) => {
    try {
      const newTask = await RecurringTaskService.createRecurringTask(userId, taskData);
      setRecurringTasks([...recurringTasks, newTask]);
      setShowForm(false);
    } catch (err) {
      setError('Failed to create recurring task');
      console.error('Error creating recurring task:', err);
    }
  };

  const handleUpdateSubmit = async (taskData: Partial<Omit<RecurringTask, 'id' | 'userId' | 'createdAt' | 'updatedAt'>>) => {
    if (!editingTask) return;

    try {
      const updatedTask = await RecurringTaskService.updateRecurringTask(userId, editingTask.id, taskData);
      setRecurringTasks(recurringTasks.map(t => t.id === updatedTask.id ? updatedTask : t));
      setEditingTask(null);
      setShowForm(false);
    } catch (err) {
      setError('Failed to update recurring task');
      console.error('Error updating recurring task:', err);
    }
  };

  const handleEdit = (task: RecurringTask) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleDelete = async (taskId: number) => {
    try {
      await RecurringTaskService.deleteRecurringTask(userId, taskId);
      setRecurringTasks(recurringTasks.filter(t => t.id !== taskId));
    } catch (err) {
      setError('Failed to delete recurring task');
      console.error('Error deleting recurring task:', err);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-32">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Recurring Tasks</h1>
        <button
          onClick={() => setShowForm(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Create New
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {showForm ? (
        <RecurringTaskForm
          onSubmit={editingTask ? handleUpdateSubmit : handleCreateSubmit}
          onCancel={handleCancel}
          recurringTask={editingTask || undefined}
        />
      ) : (
        <div className="space-y-4">
          {recurringTasks.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No recurring tasks found. Create one to get started!</p>
            </div>
          ) : (
            recurringTasks.map((task) => (
              <div key={task.id} className="bg-white p-4 rounded-lg shadow border border-gray-200">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-lg text-gray-800">{task.title}</h3>
                    <p className="text-gray-600 mt-1">{task.description}</p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {task.frequency} every {task.interval}
                      </span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        task.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {task.active ? 'Active' : 'Inactive'}
                      </span>
                      {task.endDate && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          Ends: {new Date(task.endDate).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(task)}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default RecurringTaskManager;