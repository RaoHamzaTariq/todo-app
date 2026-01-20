"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Archive, Trash2, CheckCircle2, Clock, Star, RotateCcw, Filter, Search } from "lucide-react";
import { Task } from "@/types/task";
import Link from "next/link";

export default function ArchivePage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'completed' | 'archived'>('completed');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function fetchTasks() {
      try {
        setLoading(true);
        const response = await fetch("/api/tasks");
        if (!response.ok) {
          throw new Error(`Failed to load tasks: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        const tasksData = Array.isArray(data.tasks) ? data.tasks : data;

        // For now, treating all completed tasks as archived
        // In a real implementation, you might have a separate archived field
        setTasks(tasksData);
      } catch (err: any) {
        console.error("Failed to load tasks", err);
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, []);

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'archived') return task.completed; // In this implementation, archived = completed
    return true; // 'all'
  });

  // Filter tasks based on search query
  const searchedTasks = filteredTasks.filter(task =>
    task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"
        />
        <p className="text-gray-500 font-bold">Loading archived tasks...</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <Archive className="w-8 h-8 text-blue-500" />
          StructDo Archive
        </h1>
        <p className="text-gray-600 dark:text-gray-400">View your completed and archived tasks</p>
      </div>

      {/* Header with search and filters */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">
              Archived Tasks
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2 flex items-center gap-2 font-medium">
              <span className="flex h-2 w-2 rounded-full bg-blue-500"></span>
              {tasks.length} total tasks • {tasks.filter(t => t.completed).length} completed
            </p>
          </div>

          <Link href="/tasks/new">
            <motion.button
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              className="w-full lg:w-auto flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-3.5 px-8 rounded-2xl font-bold shadow-xl shadow-blue-500/20 hover:shadow-blue-500/30 transition-all"
            >
              <CheckCircle2 className="w-5 h-5" />
              <span>New Active Task</span>
            </motion.button>
          </Link>
        </div>

        {/* Search and Filter Controls */}
        <div className="flex flex-col md:flex-row gap-4 mb-2">
          <div className="relative flex-1 group">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 group-focus-within:text-blue-500 transition-colors w-5 h-5" />
            <input
              type="text"
              placeholder="Search archived tasks by title or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700/50 rounded-2xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all shadow-sm"
            />
          </div>

          <div className="flex p-1.5 bg-gray-100/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-200/50 dark:border-gray-700/50 overflow-x-auto no-scrollbar">
            {(['all', 'completed'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm transition-all whitespace-nowrap ${
                  filter === f
                    ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                {f === 'completed' && <CheckCircle2 className={`w-4 h-4 ${filter === f ? 'fill-current' : ''}`} />}
                <span className="capitalize">{f}</span>
              </button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Archive Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-5 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-xl">
              <Archive className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Total Archived</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {tasks.filter(t => t.completed).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-5 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-green-100 dark:bg-green-900/20 rounded-xl">
              <CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Completed</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {tasks.filter(t => t.completed).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-5 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-xl">
              <Star className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Starred Completed</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {tasks.filter(t => t.completed && t.starred).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Task List */}
      <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">
            {searchedTasks.length} {filter === 'completed' ? 'Completed' : 'Archived'} Tasks
          </h3>
        </div>

        <AnimatePresence>
          {searchedTasks.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-16 px-4"
            >
              <div className="mx-auto w-24 h-24 flex items-center justify-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 mb-6">
                <Archive className="h-12 w-12 text-blue-500 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No archived tasks found</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                {searchQuery
                  ? `No archived tasks match your search for "${searchQuery}"`
                  : "You haven't completed any tasks yet"
                }
              </p>
              <Link href="/tasks">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium shadow-lg hover:shadow-xl transition-shadow"
                >
                  <CheckCircle2 className="w-5 h-5" />
                  View Active Tasks
                </motion.button>
              </Link>
            </motion.div>
          ) : (
            <div className="space-y-3">
              {searchedTasks.map((task) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/30 flex items-center justify-between group hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-green-100 dark:bg-green-900/20 flex items-center justify-center">
                        <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
                      </div>
                    </div>

                    <div>
                      <h4 className={`font-bold ${task.completed ? 'text-gray-500 dark:text-gray-400 line-through' : 'text-gray-900 dark:text-white'}`}>
                        {task.title}
                      </h4>
                      {task.description && (
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                          {task.description}
                        </p>
                      )}

                      <div className="flex items-center gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {new Date(task.updated_at).toLocaleDateString()}
                        </span>
                        <span className="flex items-center gap-1">
                          <Star className={`w-3 h-3 ${task.starred ? 'fill-current text-yellow-500' : ''}`} />
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)} Priority
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300"
                      title="Restore Task"
                    >
                      <RotateCcw className="w-4 h-4" />
                    </button>
                    <button
                      className="p-2 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 text-red-600 dark:text-red-400"
                      title="Delete Permanently"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </AnimatePresence>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4 mt-8">
        <Link href="/tasks/completed">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-300 dark:border-gray-700 px-6 py-3 rounded-xl font-bold shadow-sm hover:shadow-md transition-all"
          >
            <CheckCircle2 className="w-5 h-5" />
            View Completed Tasks
          </motion.button>
        </Link>

        <Link href="/tasks">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:shadow-xl transition-all"
          >
            <CheckCircle2 className="w-5 h-5" />
            View All Tasks
          </motion.button>
        </Link>
      </div>
    </div>
  );
}
