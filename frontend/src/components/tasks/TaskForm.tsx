"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

import { X, Save, ArrowLeft, Star, AlertTriangle, CheckCircle } from "lucide-react";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";

interface TaskFormProps {
  initialTitle?: string;
  initialDescription?: string;
  initialPriority?: 'low' | 'medium' | 'high';
  initialStarred?: boolean;
  taskId?: number;
  mode: "create" | "edit";
}

export default function TaskForm({
  initialTitle = "",
  initialDescription = "",
  initialPriority = 'medium',
  initialStarred = false,
  taskId,
  mode,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>(initialPriority);
  const [starred, setStarred] = useState(initialStarred);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { data: session } = authClient.useSession();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session?.user) return;

    setError(null);
    setLoading(true);

    try {
      if (mode === "create") {
        const response = await fetch('/api/tasks', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title,
            description,
            priority,
            starred
          }),
        });

        if (!response.ok) {
          throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
        }
      } else if (mode === "edit" && taskId) {
        const response = await fetch(`/api/tasks/${taskId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title,
            description,
            priority,
            starred
          }),
        });

        if (!response.ok) {
          throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
        }
      }

      router.push("/tasks");
      router.refresh();
    } catch (err: any) {
      setError(err.message || "Failed to save task");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.back();
  };

  // Priority colors
  const priorityColors = {
    low: 'text-green-600 bg-green-100 dark:bg-green-900/30',
    medium: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30',
    high: 'text-red-600 bg-red-100 dark:bg-red-900/30'
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="w-full max-w-2xl mx-auto"
    >
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 md:p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {mode === "create" ? "Create New Task" : "Edit Task"}
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              {mode === "create" ? "Add a new task to your list" : "Update your existing task"}
            </p>
          </div>
          <button
            onClick={handleCancel}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Close form"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
          >
            <p className="text-red-700 dark:text-red-300">{error}</p>
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title Field */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Task Title *
            </label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              required
              maxLength={200}
              className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700/50 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
            />
          </div>

          {/* Description Field */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700/50 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition min-h-32 resize-none"
              placeholder="Add more details about this task..."
              maxLength={1000}
            />
          </div>

          {/* Priority Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Priority
            </label>
            <div className="flex gap-3">
              {(['low', 'medium', 'high'] as const).map((level) => (
                <motion.button
                  key={level}
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setPriority(level)}
                  className={`flex-1 py-3 px-4 rounded-lg border transition-colors ${priority === level
                    ? `${priorityColors[level]} border-current font-medium`
                    : 'bg-gray-50 dark:bg-gray-700/50 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300'
                    }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    {level === 'high' && <AlertTriangle className="w-4 h-4" />}
                    {level === 'medium' && <Star className="w-4 h-4" />}
                    {level === 'low' && <CheckCircle className="w-4 h-4" />}
                    <span className="capitalize">{level}</span>
                  </div>
                </motion.button>
              ))}
            </div>
          </div>

          {/* Starred Toggle */}
          <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="flex items-center gap-3">
              <Star
                className={`w-5 h-5 cursor-pointer ${starred ? 'text-yellow-500 fill-current' : 'text-gray-400'
                  }`}
                onClick={() => setStarred(!starred)}
              />
              <div>
                <p className="font-medium text-gray-900 dark:text-white">Mark as Important</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">This task will be highlighted</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setStarred(!starred)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${starred ? 'bg-yellow-500' : 'bg-gray-300 dark:bg-gray-600'
                }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${starred ? 'translate-x-6' : 'translate-x-1'
                  }`}
              />
            </button>
          </div>

          {/* Form Actions */}
          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium shadow-lg hover:shadow-xl transition-shadow disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <motion.span
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                  />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  {mode === "create" ? "Create Task" : "Update Task"}
                </>
              )}
            </motion.button>

            <motion.button
              type="button"
              onClick={handleCancel}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 flex items-center justify-center gap-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 py-3 px-6 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Cancel
            </motion.button>
          </div>
        </form>
      </div>
    </motion.div>
  );
}