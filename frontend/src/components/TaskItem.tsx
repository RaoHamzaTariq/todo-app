"use client";

import { Task } from "@/types/task";
import Link from "next/link";
import { CheckCircle, Circle, Trash2, Edit3, Clock } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
}

export default function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  const formattedDate = new Date(task.created_at).toLocaleDateString();

  return (
    <div
      className={`p-5 bg-white rounded-xl shadow-sm border transition-all hover:shadow-md group ${task.completed ? 'border-green-200 bg-green-50' : 'border-gray-200'}`}
      role="listitem"
      aria-label={`${task.title}${task.completed ? ' (completed)' : ' (incomplete)'}`}
    >
      <div className="flex items-start gap-4">
        <button
          onClick={onToggle}
          className={`mt-0.5 flex-shrink-0 transition-colors ${task.completed ? 'text-green-500 hover:text-green-600' : 'text-gray-400 hover:text-blue-500'}`}
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          title={task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.completed ? (
            <CheckCircle className="w-6 h-6" aria-hidden="true" />
          ) : (
            <Circle className="w-6 h-6" aria-hidden="true" />
          )}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
            <div className="flex-1 min-w-0">
              <h3 className={`text-lg font-semibold break-words ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                {task.title}
              </h3>

              {task.description && (
                <p className={`mt-2 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'} break-words`}>
                  {task.description}
                </p>
              )}
            </div>

            <div className="flex gap-2 sm:gap-1 flex-shrink-0 mt-1 sm:mt-0">
              <Button
                variant="ghost"
                size="sm"
                asChild
                className="p-2 sm:p-1.5"
                aria-label="Edit task"
              >
                <Link
                  href={`/tasks/${task.id}/edit`}
                  title="Edit Task"
                >
                  <Edit3 className="w-4 h-4" aria-hidden="true" />
                  <span className="sr-only">Edit Task</span>
                </Link>
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={onDelete}
                className="p-2 sm:p-1.5"
                title="Delete Task"
                aria-label="Delete task"
              >
                <Trash2 className="w-4 h-4" aria-hidden="true" />
                <span className="sr-only">Delete Task</span>
              </Button>
            </div>
          </div>

          <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
            <span className="flex items-center gap-1" aria-label={`Created on ${formattedDate}`}>
              <Clock className="w-3.5 h-3.5" aria-hidden="true" />
              {formattedDate}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
