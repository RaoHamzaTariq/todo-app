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
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 30 }}
      className="w-full max-w-2xl mx-auto"
    >
      <div className="bg-white dark:bg-gray-800/80 backdrop-blur-xl rounded-[2rem] shadow-2xl border border-white/20 dark:border-gray-700/50 p-8 md:p-10 relative overflow-hidden">
        {/* Background Accent */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-blue-500/10 blur-3xl rounded-full" />
        <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-purple-500/10 blur-3xl rounded-full" />

        {/* Header */}
        <div className="flex items-center justify-between mb-10 relative z-10">
          <div>
            <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight">
              {mode === "create" ? "Create New Task" : "Edit Task"}
            </h2>
            <p className="text-gray-500 dark:text-gray-400 mt-2 font-medium">
              {mode === "create" ? "Design your next accomplishment" : "Refine your existing objective"}
            </p>
          </div>
          <button
            onClick={handleCancel}
            className="p-3 rounded-2xl bg-gray-100 dark:bg-gray-700/50 text-gray-500 hover:text-gray-900 dark:hover:text-white transition-all hover:rotate-90"
            aria-label="Close form"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-8 p-4 bg-red-500/10 border border-red-200/50 dark:border-red-800/50 rounded-2xl flex items-center gap-3"
          >
            <div className="bg-red-500 rounded-full p-1">
              <X className="w-3 h-3 text-white" />
            </div>
            <p className="text-red-700 dark:text-red-400 font-semibold text-sm">{error}</p>
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8 relative z-10">
          {/* Title Field */}
          <div className="space-y-3">
            <label htmlFor="title" className="block text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">
              Task Title
            </label>
            <div className="relative group">
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="What's the main goal?"
                required
                maxLength={200}
                className="w-full px-5 py-4 bg-gray-50 dark:bg-gray-900/50 border-2 border-gray-100 dark:border-gray-700/50 rounded-2xl focus:ring-0 focus:border-blue-500 transition-all text-lg font-medium"
              />
              <div className="absolute bottom-0 left-0 h-0.5 w-0 bg-blue-500 group-focus-within:w-full transition-all duration-300" />
            </div>
          </div>

          {/* Description Field */}
          <div className="space-y-3">
            <label htmlFor="description" className="block text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">
              Details
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-5 py-4 bg-gray-50 dark:bg-gray-900/50 border-2 border-gray-100 dark:border-gray-700/50 rounded-2xl focus:ring-0 focus:border-blue-500 transition-all min-h-32 resize-none font-medium text-gray-700 dark:text-gray-300"
              placeholder="Add more context or steps..."
              maxLength={1000}
            />
          </div>

          {/* Priority & Starred Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-3">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">
                Priority Level
              </label>
              <div className="flex p-1 bg-gray-100 dark:bg-gray-900/50 rounded-2xl border-2 border-transparent">
                {(['low', 'medium', 'high'] as const).map((level) => (
                  <button
                    key={level}
                    type="button"
                    onClick={() => setPriority(level)}
                    className={`flex-1 py-2.5 rounded-xl font-bold text-sm transition-all capitalize ${priority === level
                      ? `${priorityColors[level]} shadow-sm scale-100`
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                      }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">
                Importance
              </label>
              <button
                type="button"
                onClick={() => setStarred(!starred)}
                className={`w-full flex items-center justify-between p-3.5 rounded-2xl border-2 transition-all ${starred
                  ? 'bg-yellow-500/10 border-yellow-500/50 text-yellow-700 dark:text-yellow-400'
                  : 'bg-gray-50 dark:bg-gray-900/50 border-gray-100 dark:border-gray-700/50 text-gray-500'
                  }`}
              >
                <div className="flex items-center gap-3">
                  <Star className={`w-5 h-5 ${starred ? 'fill-current' : ''}`} />
                  <span className="font-bold">Important</span>
                </div>
                <div className={`w-6 h-6 rounded-full flex items-center justify-center transition-all ${starred ? 'bg-yellow-500 text-white' : 'bg-gray-300 dark:bg-gray-600'
                  }`}>
                  {starred && <CheckCircle className="w-4 h-4" />}
                </div>
              </button>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex flex-col sm:flex-row gap-4 pt-6">
            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-[2] flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-4 px-8 rounded-2xl font-bold shadow-xl shadow-blue-500/20 hover:shadow-blue-500/30 transition-all disabled:opacity-50"
            >
              {loading ? (
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="w-5 h-5 border-3 border-white border-t-transparent rounded-full"
                />
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  <span>{mode === "create" ? "Launch Task" : "Commit Changes"}</span>
                </>
              )}
            </motion.button>

            <motion.button
              type="button"
              onClick={handleCancel}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 flex items-center justify-center gap-2 bg-gray-100 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300 py-4 px-6 rounded-2xl font-bold hover:bg-gray-200 dark:hover:bg-gray-600 transition-all"
            >
              Cancel
            </motion.button>
          </div>
        </form>
      </div>
    </motion.div>
  );
}
