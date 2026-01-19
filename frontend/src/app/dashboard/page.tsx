"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CheckCircle, Clock, Star, BarChart3 } from "lucide-react";
import { Task } from "@/types/task";
import Link from "next/link";

export default function DashboardPage() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchTasks() {
            try {
                const response = await fetch("/api/tasks");
                if (response.ok) {
                    const data = await response.json();
                    setTasks(Array.isArray(data.tasks) ? data.tasks : data);
                }
            } catch (err) {
                console.error("Failed to fetch tasks for dashboard", err);
            } finally {
                setLoading(false);
            }
        }
        fetchTasks();
    }, []);

    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;
    const starred = tasks.filter(t => t.starred).length;

    const stats = [
        { label: "Total Tasks", value: total, icon: BarChart3, color: "text-blue-600", bg: "bg-blue-100" },
        { label: "Completed", value: completed, icon: CheckCircle, color: "text-green-600", bg: "bg-green-100" },
        { label: "Pending", value: pending, icon: Clock, color: "text-yellow-600", bg: "bg-yellow-100" },
        { label: "Important", value: starred, icon: Star, color: "text-purple-600", bg: "bg-purple-100" },
    ];

    if (loading) return <div className="text-center py-20">Loading dashboard...</div>;

    return (
        <div className="w-full">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
                <p className="text-gray-600 dark:text-gray-400">Welcome back! Here's an overview of your tasks.</p>
            </header>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                {stats.map((stat, index) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className={`p-3 rounded-xl ${stat.bg} ${stat.color}`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                        </div>
                        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">{stat.label}</h3>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{stat.value}</p>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent Tasks */}
                <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">Recent Tasks</h3>
                        <Link href="/tasks" className="text-sm text-blue-600 hover:underline">View All</Link>
                    </div>
                    <div className="space-y-4">
                        {tasks.slice(0, 5).map(task => (
                            <div key={task.id} className="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                                <div className="flex items-center gap-3">
                                    <div className={`w-2 h-2 rounded-full ${task.completed ? 'bg-green-500' : 'bg-blue-500'}`} />
                                    <span className={`text-sm font-medium ${task.completed ? 'text-gray-400 line-through' : 'text-gray-700 dark:text-gray-300'}`}>
                                        {task.title}
                                    </span>
                                </div>
                                {task.starred && <Star className="w-4 h-4 text-yellow-500 fill-current" />}
                            </div>
                        ))}
                        {tasks.length === 0 && <p className="text-gray-500 text-center py-4">No tasks yet.</p>}
                    </div>
                </div>

                {/* Motivation Card */}
                <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-8 rounded-2xl shadow-lg text-white flex flex-col justify-between">
                    <div>
                        <h3 className="text-2xl font-bold mb-4">You're doing great!</h3>
                        <p className="text-blue-100 text-lg">
                            {completed > 0
                                ? `You've completed ${completed} tasks so far. Keep the momentum going!`
                                : "Ready to start your first task? Let's make today productive!"
                            }
                        </p>
                    </div>
                    <Link href="/tasks/new">
                        <button className="mt-8 bg-white text-blue-600 px-6 py-3 rounded-xl font-bold hover:bg-blue-50 transition-colors w-full sm:w-auto">
                            Create New Task
                        </button>
                    </Link>
                </div>
            </div>
        </div>
    );
}
