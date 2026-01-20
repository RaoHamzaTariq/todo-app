"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Calendar as CalendarIcon, Plus, Clock, CheckCircle2, Star, Search, Filter } from "lucide-react";
import { Task } from "@/types/task";
import Link from "next/link";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";

type ValuePiece = Date | null;
type Value = ValuePiece | [ValuePiece, ValuePiece];

export default function CalendarPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [date, setDate] = useState<Value>(new Date());
  const [loading, setLoading] = useState(true);
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

        // Filter to only show incomplete tasks for calendar view
        const incompleteTasks = tasksData.filter((task: Task) => !task.completed);
        setTasks(incompleteTasks);
        setFilteredTasks(incompleteTasks);
      } catch (err: any) {
        console.error("Failed to load tasks", err);
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, []);

  // Filter tasks based on selected date and search query
  useEffect(() => {
    if (!date || Array.isArray(date)) return;

    const selectedDate = new Date(date);
    // Format selected date to YYYY-MM-DD to compare with task dates
    const selectedDateString = selectedDate.toISOString().split('T')[0];

    let tasksForSelectedDate = tasks.filter(task => {
      // Compare creation date with selected date (could be enhanced to use due dates if available)
      const taskDate = new Date(task.created_at).toISOString().split('T')[0];
      return taskDate === selectedDateString;
    });

    // Apply search filter
    if (searchQuery) {
      tasksForSelectedDate = tasksForSelectedDate.filter(task =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    setFilteredTasks(tasksForSelectedDate);
  }, [date, tasks, searchQuery]);

  const handleDateChange = (value: Value) => {
    setDate(value);
  };

  // Group tasks by priority for display
  const groupedTasks = filteredTasks.reduce((acc, task) => {
    if (!acc[task.priority]) {
      acc[task.priority] = [];
    }
    acc[task.priority].push(task);
    return acc;
  }, {} as Record<string, Task[]>);

  // Helper function to get display date
  const getDisplayDate = () => {
    if (!date) return 'No Date Selected';
    if (Array.isArray(date)) return 'Selected Dates';
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"
        />
        <p className="text-gray-500 font-bold">Loading calendar...</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <CalendarIcon className="w-8 h-8 text-blue-500" />
          StructDo Calendar
        </h1>
        <p className="text-gray-600 dark:text-gray-400">Visualize your tasks over time</p>
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
              Calendar View
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2 flex items-center gap-2 font-medium">
              <span className="flex h-2 w-2 rounded-full bg-blue-500"></span>
              {tasks.length} scheduled tasks • {tasks.filter(t => t.completed).length} completed
            </p>
          </div>

          <Link href="/tasks/new">
            <motion.button
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              className="w-full lg:w-auto flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-3.5 px-8 rounded-2xl font-bold shadow-xl shadow-blue-500/20 hover:shadow-blue-500/30 transition-all"
            >
              <Plus className="w-5 h-5" />
              <span>Create New Task</span>
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
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Calendar Section */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Select Date</h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
              Click on a date to view tasks scheduled for that day
            </p>
          </div>

          <div className="bg-white dark:bg-gray-900/50 p-4 rounded-2xl border border-gray-200 dark:border-gray-700">
            <style jsx global>{`
              .react-calendar {
                width: 100%;
                border: none;
                background: transparent;
              }

              .react-calendar__navigation {
                margin-bottom: 1rem;
              }

              .react-calendar__navigation button {
                min-width: 44px;
                padding: 0.5rem;
                border-radius: 0.75rem;
                background: transparent;
                color: inherit;
                font-weight: bold;
                font-size: 1rem;
                line-height: 1.25rem;
              }

              .react-calendar__navigation button:hover {
                background-color: rgba(156, 163, 175, 0.1);
              }

              .react-calendar__month-view__weekdays {
                text-align: center;
                font-weight: bold;
                font-size: 0.75rem;
                line-height: 1rem;
                color: #6b7280;
              }

              .react-calendar__month-view__weekdays__weekday {
                padding: 0.5rem 0;
              }

              .react-calendar__month-view__days {
                padding: 0.25rem;
              }

              .react-calendar__tile {
                max-width: 100%;
                text-align: center;
                padding: 0.75rem 0.25rem;
                border-radius: 0.75rem;
                transition: all 0.2s;
                position: relative;
              }

              .react-calendar__tile:enabled:hover {
                background-color: rgba(156, 163, 175, 0.1);
              }

              .react-calendar__tile--now {
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                color: white;
                font-weight: bold;
              }

              .react-calendar__tile--active {
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                color: white;
                font-weight: bold;
              }

              .react-calendar__tile--range {
                background-color: rgba(59, 130, 246, 0.1);
              }

              .react-calendar__tile--rangeStart {
                border-top-left-radius: 0.75rem;
                border-bottom-left-radius: 0.75rem;
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                color: white;
              }

              .react-calendar__tile--rangeEnd {
                border-top-right-radius: 0.75rem;
                border-bottom-right-radius: 0.75rem;
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                color: white;
              }

              .react-calendar__tile--has-tasks::after {
                content: '';
                position: absolute;
                bottom: 0.25rem;
                left: 50%;
                transform: translateX(-50%);
                width: 4px;
                height: 4px;
                background-color: #3b82f6;
                border-radius: 50%;
              }

              .react-calendar__tile--weekend {
                color: #ef4444;
              }

              .react-calendar__month-view__days__day--neighboringMonth {
                color: #9ca3af;
              }

              .dark .react-calendar__navigation button:hover {
                background-color: rgba(75, 85, 99, 0.2);
              }

              .dark .react-calendar__tile:enabled:hover {
                background-color: rgba(75, 85, 99, 0.2);
              }

              .dark .react-calendar__month-view__weekdays {
                color: #9ca3af;
              }

              .dark .react-calendar__month-view__days__day--neighboringMonth {
                color: #4b5563;
              }
            `}</style>
            <Calendar
              onChange={handleDateChange}
              value={date}
              locale="en-US"
              className="w-full border-0"
              tileClassName={({ date: tileDate, view }) => {
                // Highlight days that have tasks
                const dateString = tileDate.toISOString().split('T')[0];
                const hasTasks = tasks.some(task => {
                  const taskDate = new Date(task.created_at).toISOString().split('T')[0];
                  return taskDate === dateString;
                });

                // Determine if it's today
                const today = new Date();
                const isToday = tileDate.getDate() === today.getDate() &&
                  tileDate.getMonth() === today.getMonth() &&
                  tileDate.getFullYear() === today.getFullYear();

                let classes = 'react-calendar__tile ';

                if (hasTasks) {
                  classes += 'react-calendar__tile--has-tasks ';
                }

                if (isToday) {
                  classes += 'react-calendar__tile--now ';
                }

                return classes;
              }}
            />
          </div>
        </div>

        {/* Tasks Section */}
        <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              {getDisplayDate()}
            </h2>

            <Link href="/tasks/new">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg font-bold shadow-lg"
              >
                <Plus className="w-4 h-4" />
                <span className="text-sm">New Task</span>
              </motion.button>
            </Link>
          </div>

          <AnimatePresence>
            {filteredTasks.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-12"
              >
                <div className="mx-auto w-16 h-16 flex items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900/20 mb-4">
                  <CalendarIcon className="h-8 w-8 text-blue-500 dark:text-blue-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">No tasks for this date</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Schedule a task to appear on this date
                </p>
              </motion.div>
            ) : (
              <div className="space-y-6">
                {['high', 'medium', 'low'].map(priority => {
                  if (!groupedTasks[priority] || groupedTasks[priority].length === 0) return null;

                  return (
                    <div key={priority} className="space-y-3">
                      <div className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full ${priority === 'high' ? 'bg-red-500' :
                            priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                          }`}></div>
                        <h3 className="font-bold text-gray-900 dark:text-white capitalize">
                          {priority} Priority
                        </h3>
                        <span className="text-gray-500 dark:text-gray-400 text-sm">
                          ({groupedTasks[priority].length})
                        </span>
                      </div>

                      <div className="space-y-2">
                        {groupedTasks[priority].map(task => (
                          <motion.div
                            key={task.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/30 hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
                          >
                            <div className="flex items-start justify-between">
                              <div>
                                <h4 className="font-bold text-gray-900 dark:text-white">{task.title}</h4>
                                {task.description && (
                                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                                    {task.description}
                                  </p>
                                )}
                              </div>
                              {task.starred && (
                                <Star className="w-4 h-4 text-yellow-500 fill-current flex-shrink-0 ml-2" />
                              )}
                            </div>
                            <div className="flex items-center gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                              <span className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {new Date(task.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                              </span>
                              <span className="flex items-center gap-1">
                                <CheckCircle2 className="w-3 h-3" />
                                {task.completed ? 'Completed' : 'Pending'}
                              </span>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Additional Task Insights */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-5 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-xl">
              <CalendarIcon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Total Scheduled</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{tasks.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-5 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-green-100 dark:bg-green-900/20 rounded-xl">
              <CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Completed Today</p>
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
              <p className="text-sm text-gray-500 dark:text-gray-400">High Priority</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {tasks.filter(t => t.priority === 'high').length}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}