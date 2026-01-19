"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import { createAuthClient } from "better-auth/react"
import Button from "./ui/Button";
import Input from "./ui/Input";
import Card from "./ui/Card";

interface TaskFormProps {
  initialTitle?: string;
  initialDescription?: string;
  taskId?: number;
  mode: "create" | "edit";
}

export default function TaskForm({
  initialTitle = "",
  initialDescription = "",
  taskId,
  mode,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const {useSession} = createAuthClient()
  const {
        data: session
    } = useSession()

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
          body: JSON.stringify({ title, description }),
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
          body: JSON.stringify({ title, description }),
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

  return (
    <Card className="p-6" role="region" aria-labelledby="form-heading">
      <h2 id="form-heading" className="text-2xl font-bold text-gray-900 mb-6">
        {mode === "create" ? "Create New Task" : "Edit Task"}
      </h2>

      {error && (
        <div
          className="mb-6 p-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg"
          role="alert"
          aria-live="assertive"
        >
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label="Task Title *"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          required
          maxLength={200}
          error={error ? error : undefined}
          aria-required="true"
        />

        <div>
          <label htmlFor="task-description" className="block mb-2 text-sm font-medium text-gray-700">Description</label>
          <textarea
            id="task-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none min-h-32 text-base"
            placeholder="Add more details about this task..."
            maxLength={1000}
            aria-describedby="description-help-text"
          />
          <p id="description-help-text" className="mt-1 text-sm text-gray-500">
            Optional description for your task (max 1000 characters)
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <Button
            type="submit"
            loading={loading}
            disabled={loading}
            variant="primary"
            size="lg"
            className="flex-1 py-3"
            aria-busy={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : mode === "create" ? "Create Task" : "Update Task"}
          </Button>
          <Button
            type="button"
            onClick={() => router.back()}
            variant="secondary"
            size="lg"
            className="flex-1 py-3"
          >
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  );
}