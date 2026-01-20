"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence, LayoutGroup } from "framer-motion";
import { Plus, Search, CheckCircle, Star } from "lucide-react";
import { Task } from "@/types/task";
import TaskItem from "./TaskItem";
import DeleteConfirmation from "../DeleteConfirmation";
import Link from "next/link";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { y: 20, opacity: 0 },
  show: { y: 0, opacity: 1 }
};

export default function TaskList({ defaultFilter = 'all' }: { defaultFilter?: 'all' | 'active' | 'completed' | 'starred' }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed' | 'starred'>(defaultFilter);
  const [searchQuery, setSearchQuery] = useState('');
  const [deleteTaskId, setDeleteTaskId] = useState<number | null>(null);


  // Fetch tasks once session is available
  useEffect(() => {

    async function fetchTasks() {
      try {
        setLoading(true);
        const response = await fetch("/api/tasks");
        if (!response.ok) {
          throw new Error(`Failed to load tasks: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        setTasks(Array.isArray(data.tasks) ? data.tasks : data);
      } catch (err: any) {
        setError(err.message || "Failed to load tasks");
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();

  }, []);

  const handleToggle = async (taskId: number) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}/complete`, {
        method: 'PATCH',
      });

      if (response.ok) {
        setTasks((prev) =>
          prev.map((t) => (t.id === taskId ? { ...t, completed: !t.completed } : t))
        );
      } else {
        throw new Error(`Failed to toggle task: ${response.status} ${response.statusText}`);
      }
    } catch (err) {
      console.error("Failed to toggle task", err);
    }
  };


  const initDelete = (taskId: number) => {
    setDeleteTaskId(taskId);
  };

  const confirmDelete = async () => {
    if (!deleteTaskId) return;

    try {
      const response = await fetch(`/api/tasks/${deleteTaskId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== deleteTaskId));
        setDeleteTaskId(null);
      } else {
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }
    } catch (err) {
      console.error("Failed to delete task", err);
    }
  };

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    if (filter === 'starred') return task.starred;
    return true; // 'all'
  });

  // Filter tasks based on search query
  const searchedTasks = filteredTasks.filter(task =>
    task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  if (loading) return (
    <div className="flex justify-center items-center py-16 w-full">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
      />
    </div>
  );

  if (error) return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center p-8 bg-red-50 dark:bg-red-900/20 rounded-xl border border-red-200 dark:border-red-800"
    >
      <p className="text-red-600 dark:text-red-400 text-lg mb-4">{error}</p>
      <button
        onClick={() => window.location.reload()}
        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
      >
        Retry
      </button>
    </motion.div>
  );

  return (
    <div className="w-full">
      {/* Header with search and filters */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-8">
          <div>
            <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white tracking-tight">
              My Tasks
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2 flex items-center gap-2 font-medium">
              <span className="flex h-2 w-2 rounded-full bg-blue-500"></span>
              {tasks.length} tasks • {tasks.filter(t => t.completed).length} completed
            </p>
          </div>

          <Link href="/tasks/new">
            <motion.button
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              className="w-full lg:w-auto flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-3.5 px-8 rounded-2xl font-bold shadow-xl shadow-blue-500/20 hover:shadow-blue-500/30 transition-all"
            >
              <Plus className="w-5 h-5" />
              <span>Create Task</span>
            </motion.button>
          </Link>
        </div>

        {/* Search and Filter Controls */}
        <div className="flex flex-col md:flex-row gap-4 mb-2">
          <div className="relative flex-1 group">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 group-focus-within:text-blue-500 transition-colors w-5 h-5" />
            <input
              type="text"
              placeholder="Search tasks by title or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all shadow-sm"
            />
          </div>

          <div className="flex p-1.5 bg-gray-100/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-200/50 dark:border-gray-700/50 overflow-x-auto no-scrollbar">
            {(['all', 'active', 'completed', 'starred'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm transition-all whitespace-nowrap ${filter === f
                  ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                  }`}
              >
                {f === 'starred' && <Star className={`w-4 h-4 ${filter === f ? 'fill-current' : ''}`} />}
                <span className="capitalize">{f}</span>
              </button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Task List */}
      <LayoutGroup>
        {searchedTasks.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-16 px-4"
          >
            <div className="mx-auto w-24 h-24 flex items-center justify-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 mb-6">
              <CheckCircle className="h-12 w-12 text-blue-500 dark:text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No tasks found</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {searchQuery
                ? `No tasks match your search for "${searchQuery}"`
                : filter === 'completed'
                  ? "You haven't completed any tasks yet"
                  : filter === 'active'
                    ? "All tasks are completed! Great job!"
                    : "Get started by creating your first task"
              }
            </p>
            <Link href="/tasks/new">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium shadow-lg hover:shadow-xl transition-shadow"
              >
                <Plus className="w-5 h-5" />
                Create New Task
              </motion.button>
            </Link>
          </motion.div>
        ) : (
          <motion.div
            variants={container}
            initial="hidden"
            animate="show"
            className="space-y-3"
          >
            <AnimatePresence>
              {searchedTasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onToggle={() => handleToggle(task.id)}
                  onDelete={() => initDelete(task.id)}
                />
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </LayoutGroup>

      <DeleteConfirmation
        isOpen={!!deleteTaskId}
        onClose={() => setDeleteTaskId(null)}
        onConfirm={confirmDelete}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
      />
    </div>
  );
}