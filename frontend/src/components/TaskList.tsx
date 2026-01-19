"use client";

import { useEffect, useState } from "react";
import { authClient } from "@/lib/auth-client";
import { Task } from "@/types/task";
import TaskItem from "./TaskItem";
import Link from "next/link";
import {Button} from "./ui/Button";
import {Card} from "./ui/Card";

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<any>(null);

  // Fetch session once on mount
  useEffect(() => {
    let mounted = true;

    async function fetchSession() {
      const data = await authClient.getSession();
      if (mounted) setSession(data);
    }

    fetchSession();

    return () => {
      mounted = false;
    };
  }, []);

  // Fetch tasks once session is available
  useEffect(() => {
    if (!session?.user) return;

    let mounted = true;

    async function fetchTasks() {
      try {
        setLoading(true);
        const response = await fetch('/api/tasks');
        if (!response.ok) {
          throw new Error(`Failed to load tasks: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        if (mounted) setTasks(Array.isArray(data.tasks) ? data.tasks : data);
      } catch (err: any) {
        if (mounted) setError(err.message || "Failed to load tasks");
      } finally {
        if (mounted) setLoading(false);
      }
    }

    fetchTasks();

    return () => {
      mounted = false;
    };
  }, [session]);

  const handleToggle = async (taskId: number) => {
    if (!session?.user) return;

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

  const handleDelete = async (taskId: number) => {
    if (!session?.user) return;
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== taskId));
      } else {
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }
    } catch (err) {
      console.error("Failed to delete task", err);
    }
  };

  if (loading) return (
    <div className="flex justify-center items-center py-16 w-full">
      <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-blue-500"></div>
    </div>
  );

  if (error) return (
    <Card className="text-center p-8 w-full">
      <div className="text-red-600 text-lg mb-4">{error}</div>
      <Button
        variant="secondary"
        onClick={() => window.location.reload()}
      >
        Retry
      </Button>
    </Card>
  );

  return (
    <div className="w-full" role="main" aria-label="Task management">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="text-gray-600 mt-2">
            {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} •{" "}
            {tasks.filter(t => t.completed).length} completed
          </p>
        </div>
        <Button
          variant="primary"
          size="lg"
          asChild
          className="w-full md:w-auto"
          aria-label="Add new task"
        >
          <Link href="/tasks/new" className="flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            Add New Task
          </Link>
        </Button>
      </div>

      {tasks.length === 0 ? (
        <Card className="text-center py-16 px-4">
          <div className="mx-auto w-24 h-24 flex items-center justify-center rounded-full bg-blue-50 mb-6" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No tasks yet</h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Get started by creating your first task. You'll be able to organize, track, and complete your tasks efficiently.
          </p>
          <Button
            variant="primary"
            size="lg"
            asChild
            aria-label="Create your first task"
          >
            <Link href="/tasks/new" className="flex items-center justify-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Create Your First Task
            </Link>
          </Button>
        </Card>
      ) : (
        <div className="space-y-4" role="list" aria-label="List of tasks">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={() => handleToggle(task.id)}
              onDelete={() => handleDelete(task.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
