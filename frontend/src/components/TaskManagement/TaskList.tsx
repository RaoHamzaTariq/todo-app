import React, { useState, useEffect, useMemo } from 'react';
import { Task } from '../../types/task';
import TaskService from '../../services/taskService';
import './TaskList.css';

interface TaskListProps {
  userId: string;
  onTaskUpdate?: (task: Task) => void;
  onTaskDelete?: (taskId: number) => void;
}

interface FilterOptions {
  status: string;
  priority: string;
  searchQuery: string;
  tag: string;
}

interface SortOptions {
  sortBy: 'createdAt' | 'updatedAt' | 'dueDate' | 'priority';
  order: 'asc' | 'desc';
}

const TaskList: React.FC<TaskListProps> = ({ userId, onTaskUpdate, onTaskDelete }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    status: 'all',
    priority: 'all',
    searchQuery: '',
    tag: ''
  });
  const [sortOptions, setSortOptions] = useState<SortOptions>({
    sortBy: 'createdAt',
    order: 'desc'
  });
  const [showFilters, setShowFilters] = useState<boolean>(false);

  // Fetch tasks from the API
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const userTasks = await TaskService.getTasks(userId);
        setTasks(userTasks);
        setError(null);
      } catch (err) {
        setError('Failed to load tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  // Apply filters and sorting to tasks
  const filteredAndSortedTasks = useMemo(() => {
    let result = [...tasks];

    // Apply status filter
    if (filterOptions.status !== 'all') {
      result = result.filter(task => task.status === filterOptions.status);
    }

    // Apply priority filter
    if (filterOptions.priority !== 'all') {
      result = result.filter(task => task.priority === filterOptions.priority);
    }

    // Apply tag filter
    if (filterOptions.tag) {
      const lowerTag = filterOptions.tag.toLowerCase();
      result = result.filter(task =>
        task.tags.some(tag => tag.toLowerCase().includes(lowerTag))
      );
    }

    // Apply search query filter
    if (filterOptions.searchQuery) {
      const query = filterOptions.searchQuery.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(query) ||
        (task.description && task.description.toLowerCase().includes(query))
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      let aValue: any, bValue: any;

      switch (sortOptions.sortBy) {
        case 'createdAt':
          aValue = new Date(a.created_at).getTime();
          bValue = new Date(b.created_at).getTime();
          break;
        case 'updatedAt':
          aValue = new Date(a.updated_at).getTime();
          bValue = new Date(b.updated_at).getTime();
          break;
        case 'dueDate':
          aValue = a.due_date ? new Date(a.due_date).getTime() : Infinity;
          bValue = b.due_date ? new Date(b.due_date).getTime() : Infinity;
          break;
        case 'priority':
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          aValue = priorityOrder[a.priority as keyof typeof priorityOrder];
          bValue = priorityOrder[b.priority as keyof typeof priorityOrder];
          break;
        default:
          aValue = new Date(a.created_at).getTime();
          bValue = new Date(b.created_at).getTime();
      }

      if (sortOptions.order === 'asc') {
        return aValue - bValue;
      } else {
        return bValue - aValue;
      }
    });

    return result;
  }, [tasks, filterOptions, sortOptions]);

  // Handle task completion toggle
  const handleToggleCompletion = async (task: Task) => {
    try {
      const updatedTask = await TaskService.toggleTaskCompletion(userId, task.id);
      setTasks(prev => prev.map(t => t.id === task.id ? updatedTask : t));

      if (onTaskUpdate) {
        onTaskUpdate(updatedTask);
      }
    } catch (err) {
      setError('Failed to update task completion');
      console.error('Error toggling task completion:', err);
    }
  };

  // Handle task deletion
  const handleDeleteTask = async (taskId: number) => {
    try {
      await TaskService.deleteTask(userId, taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));

      if (onTaskDelete) {
        onTaskDelete(taskId);
      }
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  // Handle filter changes
  const handleFilterChange = (field: keyof FilterOptions, value: string) => {
    setFilterOptions(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Handle sort changes
  const handleSortChange = (field: keyof SortOptions, value: string) => {
    setSortOptions(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Group tasks by status for better visualization
  const groupedTasks = useMemo(() => {
    return filteredAndSortedTasks.reduce((acc, task) => {
      if (!acc[task.status]) {
        acc[task.status] = [];
      }
      acc[task.status].push(task);
      return acc;
    }, {} as Record<string, Task[]>);
  }, [filteredAndSortedTasks]);

  if (loading) {
    return (
      <div className="task-list-loading">
        <div className="spinner"></div>
        <p>Loading tasks...</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      <div className="task-list-header">
        <h2>Tasks ({filteredAndSortedTasks.length})</h2>

        <button
          className="toggle-filters-btn"
          onClick={() => setShowFilters(!showFilters)}
        >
          {showFilters ? 'Hide Filters' : 'Show Filters'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Filters Panel */}
      {showFilters && (
        <div className="filters-panel">
          <div className="filter-group">
            <label htmlFor="status-filter">Status:</label>
            <select
              id="status-filter"
              value={filterOptions.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="in-progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="priority-filter">Priority:</label>
            <select
              id="priority-filter"
              value={filterOptions.priority}
              onChange={(e) => handleFilterChange('priority', e.target.value)}
            >
              <option value="all">All Priorities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="tag-filter">Tag:</label>
            <input
              type="text"
              id="tag-filter"
              placeholder="Filter by tag..."
              value={filterOptions.tag}
              onChange={(e) => handleFilterChange('tag', e.target.value)}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="search-query">Search:</label>
            <input
              type="text"
              id="search-query"
              placeholder="Search tasks..."
              value={filterOptions.searchQuery}
              onChange={(e) => handleFilterChange('searchQuery', e.target.value)}
            />
          </div>

          <div className="sort-options">
            <div className="filter-group">
              <label htmlFor="sort-by">Sort by:</label>
              <select
                id="sort-by"
                value={sortOptions.sortBy}
                onChange={(e) => handleSortChange('sortBy', e.target.value as any)}
              >
                <option value="createdAt">Created At</option>
                <option value="updatedAt">Updated At</option>
                <option value="dueDate">Due Date</option>
                <option value="priority">Priority</option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="sort-order">Order:</label>
              <select
                id="sort-order"
                value={sortOptions.order}
                onChange={(e) => handleSortChange('order', e.target.value as any)}
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Task List */}
      <div className="tasks-container">
        {filteredAndSortedTasks.length === 0 ? (
          <div className="no-tasks">
            <p>No tasks found matching your criteria.</p>
          </div>
        ) : (
          <div className="tasks-grid">
            {filteredAndSortedTasks.map(task => (
              <div
                key={task.id}
                className={`task-card ${task.completed ? 'completed' : ''} priority-${task.priority}`}
              >
                <div className="task-header">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleCompletion(task)}
                    className="task-checkbox"
                  />

                  <h3 className="task-title">{task.title}</h3>

                  <button
                    className="delete-btn"
                    onClick={() => handleDeleteTask(task.id)}
                    aria-label="Delete task"
                  >
                    ×
                  </button>
                </div>

                {task.description && (
                  <p className="task-description">{task.description}</p>
                )}

                <div className="task-meta">
                  {task.due_date && (
                    <span className="due-date">
                      Due: {new Date(task.due_date).toLocaleDateString()}
                    </span>
                  )}

                  <span className={`priority-badge priority-${task.priority}`}>
                    {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                  </span>

                  <span className={`status-badge status-${task.status}`}>
                    {task.status.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                </div>

                <div className="task-tags">
                  {task.tags.map((tag, index) => (
                    <span key={index} className="tag">
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskList;