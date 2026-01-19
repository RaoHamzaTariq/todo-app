"use client";

import TaskList from "@/components/tasks/TaskList";

export default function ImportantTasksPage() {
    return (
        <div className="w-full">
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Important Tasks</h1>
                <p className="text-gray-600 dark:text-gray-400">Tasks you've marked as important</p>
            </div>
            <TaskList defaultFilter="starred" />
        </div>
    );
}
