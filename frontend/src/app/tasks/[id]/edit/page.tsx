"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import TaskForm from "@/components/tasks/TaskForm";
import { authClient } from "@/lib/auth-client";
import { Task } from "@/types/task";

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

  if (loading) return <div className="text-center py-20">Loading...</div>;
  if (error || !task) return <div className="text-center py-20 text-red-600">{error || "Task not found"}</div>;

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-8">
      <div className="max-w-xl mx-auto">
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
