"use client";

import TaskList from "@/components/tasks/TaskList";

export default function CompletedTasksPage() {
    return (
        <div className="w-full">
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Completed Tasks</h1>
                <p className="text-gray-600 dark:text-gray-400">Your accomplishments</p>
            </div>
            <TaskList defaultFilter="completed" />
        </div>
    );
}
