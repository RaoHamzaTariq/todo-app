"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Task } from "@/types/task";
import { Button } from "@/components/ui/Button";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Edit3,
  CheckCircle,
  Circle,
  Calendar,
  Star,
  AlertCircle
} from "lucide-react";

export default function TaskDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTask() {
      try {
        setLoading(true);
        const response = await fetch(`/api/tasks/${id}`);

        if (!response.ok) {
          if (response.status === 404) {
            setError("Task not found");
          } else {
            throw new Error(`Failed to load task: ${response.status} ${response.statusText}`);
          }
        } else {
          const data = await response.json();
          setTask(data);
        }
      } catch (err: any) {
        setError(err.message || "Failed to load task");
      } finally {
        setLoading(false);
      }
    }

    if (id) {
      fetchTask();
    }
  }, [id]);

  const handleToggle = async () => {
    if (!task) return;

    try {
      const response = await fetch(`/api/tasks/${task.id}/complete`, {
        method: 'PATCH',
      });

      if (response.ok) {
        const updatedTask = await response.json();
        setTask(updatedTask);
      } else {
        throw new Error(`Failed to toggle task: ${response.status} ${response.statusText}`);
      }
    } catch (err) {
      console.error("Failed to toggle task", err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-16 w-full">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center p-8 bg-red-50 dark:bg-red-900/20 rounded-xl border border-red-200 dark:border-red-800"
      >
        <p className="text-red-600 dark:text-red-400 text-lg mb-4">{error}</p>
        <Button
          onClick={() => router.back()}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Go Back
        </Button>
      </motion.div>
    );
  }

  if (!task) {
    return (
      <div className="text-center p-8">
        <p className="text-gray-600 dark:text-gray-400">Task not found</p>
        <Button
          onClick={() => router.back()}
          className="mt-4"
        >
          Go Back
        </Button>
      </div>
    );
  }

  const formattedDate = new Date(task.created_at).toLocaleDateString();
  const formattedUpdatedDate = task.updated_at ? new Date(task.updated_at).toLocaleDateString() : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto w-full"
    >
      {/* Header with back button */}
      <div className="mb-6">
        <Link href="/tasks" passHref>
          <Button variant="outline" className="flex items-center gap-2 mb-4">
            <ArrowLeft className="w-4 h-4" />
            Back to Tasks
          </Button>
        </Link>
      </div>

      {/* Task Detail Card */}
      <motion.div
        layout
        className={`p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm border ${task.completed
            ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20'
            : 'border-gray-200 dark:border-gray-700'
          }`}
      >
        <div className="flex items-start gap-4">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleToggle}
            className={`mt-1 flex-shrink-0 transition-colors ${task.completed ? 'text-green-500 hover:text-green-600' : 'text-gray-400 hover:text-blue-500'
              }`}
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
            title={task.completed ? "Mark as incomplete" : "Mark as complete"}
          >
            {task.completed ? (
              <CheckCircle className="w-6 h-6" aria-hidden="true" />
            ) : (
              <Circle className="w-6 h-6" aria-hidden="true" />
            )}
          </motion.button>

          <div className="flex-1 min-w-0">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
              <div className="flex-1 min-w-0">
                <motion.h1
                  className={`text-2xl font-bold break-words mb-4 ${task.completed
                      ? 'text-gray-500 dark:text-gray-400 line-through'
                      : 'text-gray-900 dark:text-white'
                    }`}
                >
                  {task.title}
                </motion.h1>

                {task.description && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className={`text-base ${task.completed
                        ? 'text-gray-400 dark:text-gray-500'
                        : 'text-gray-600 dark:text-gray-300'
                      } break-words whitespace-pre-wrap mb-6`}
                  >
                    {task.description}
                  </motion.div>
                )}

                {/* Task metadata */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-2" aria-label={`Created on ${formattedDate}`}>
                    <Calendar className="w-4 h-4" aria-hidden="true" />
                    <span>Created: {formattedDate}</span>
                  </div>

                  {formattedUpdatedDate && (
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4" aria-hidden="true" />
                      <span>Updated: {formattedUpdatedDate}</span>
                    </div>
                  )}

                  {task.priority === 'high' && (
                    <div className="flex items-center gap-2 text-red-500">
                      <AlertCircle className="w-4 h-4" aria-hidden="true" />
                      <span>High Priority</span>
                    </div>
                  )}

                  {task.starred && (
                    <div className="flex items-center gap-2 text-yellow-500">
                      <Star className="w-4 h-4" aria-hidden="true" />
                      <span>Important</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 flex flex-wrap gap-3">
          <Link href={`/tasks/${task.id}/edit`} passHref>
            <Button variant="outline" className="flex items-center gap-2">
              <Edit3 className="w-4 h-4" />
              Edit Task
            </Button>
          </Link>

          <Button
            onClick={() => router.back()}
            variant="secondary"
          >
            Back to Tasks
          </Button>
        </div>
      </motion.div>
    </motion.div>
  );
}