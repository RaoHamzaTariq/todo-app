"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import TaskForm from "@/components/tasks/TaskForm";
import { authClient } from "@/lib/auth-client";
import { Task } from "@/types/task";
import { motion } from "framer-motion";
import { ArrowLeft } from "lucide-react";

export default function EditTaskPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = parseInt(params.id as string);
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { data: session } = authClient.useSession();

  useEffect(() => {
    const fetchTask = async () => {
      if (!session?.user || isNaN(taskId)) return;
      try {
        const response = await fetch(`/api/tasks/${taskId}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch task: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        setTask(data);
      } catch (err: any) {
        setError("Task not found or access denied");
      } finally {
        setLoading(false);
      }
    };
    fetchTask();
  }, [session, taskId]);

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"
      />
      <p className="text-gray-600 dark:text-gray-400 font-medium">Loading task details...</p>
    </div>
  );

  if (error || !task) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
      <div className="bg-red-50 dark:bg-red-900/20 p-8 rounded-2xl border border-red-100 dark:border-red-800 text-center max-w-md w-full">
        <p className="text-red-600 dark:text-red-400 text-lg font-semibold mb-4">{error || "Task not found"}</p>
        <button
          onClick={() => router.push("/tasks")}
          className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl transition-colors font-medium"
        >
          Back to Tasks
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-transparent px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium group"
          >
            <ArrowLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" />
            Back
          </button>
        </div>
        <TaskForm
          mode="edit"
          taskId={task.id}
          initialTitle={task.title}
          initialDescription={task.description || ""}
          initialPriority={task.priority}
          initialStarred={task.starred}
        />
      </div>
    </div>
  );
}
