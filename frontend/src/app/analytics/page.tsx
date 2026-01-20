"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
    BarChart3,
    ArrowLeft,
    CheckCircle2,
    Circle,
    Star,
    AlertCircle,
    TrendingUp,
    Calendar,
    Target
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Task } from "@/types/task";
import { authClient } from "@/lib/auth-client";

export default function AnalyticsPage() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);
    const { data: session } = authClient.useSession();
    const router = useRouter();

    useEffect(() => {
        const fetchTasks = async () => {
            if (!session) return;
            try {
                const response = await fetch("/api/tasks");
                const data = await response.json();
                setTasks(data.tasks || []);
            } catch (error) {
                console.error("Failed to fetch tasks for analytics:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchTasks();
    }, [session]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mb-6"
                />
                <p className="text-gray-600 dark:text-gray-400 font-bold text-lg animate-pulse">Calculating Insights...</p>
            </div>
        );
    }

    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(t => t.completed).length;
    const pendingTasks = totalTasks - completedTasks;
    const starredTasks = tasks.filter(t => t.starred).length;
    const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

    const highPriority = tasks.filter(t => t.priority === 'high').length;
    const mediumPriority = tasks.filter(t => t.priority === 'medium').length;
    const lowPriority = tasks.filter(t => t.priority === 'low').length;

    const stats = [
        {
            label: "Total Tasks",
            value: totalTasks,
            icon: Target,
            color: "bg-blue-500",
            lightColor: "bg-blue-50 dark:bg-blue-900/20",
            textColor: "text-blue-600 dark:text-blue-400"
        },
        {
            label: "Completed",
            value: completedTasks,
            icon: CheckCircle2,
            color: "bg-green-500",
            lightColor: "bg-green-50 dark:bg-green-900/20",
            textColor: "text-green-600 dark:text-green-400"
        },
        {
            label: "Important",
            value: starredTasks,
            icon: Star,
            color: "bg-yellow-500",
            lightColor: "bg-yellow-50 dark:bg-yellow-900/20",
            textColor: "text-yellow-600 dark:text-yellow-400"
        },
        {
            label: "Completion",
            value: `${completionRate}%`,
            icon: TrendingUp,
            color: "bg-purple-500",
            lightColor: "bg-purple-50 dark:bg-purple-900/20",
            textColor: "text-purple-600 dark:text-purple-400"
        }
    ];

    return (
        <div className="max-w-7xl mx-auto px-4 py-8">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
                <div>
                    <h1 className="text-4xl font-black text-gray-900 dark:text-white tracking-tight">Performance Analytics</h1>
                    <p className="text-gray-500 dark:text-gray-400 mt-2 font-medium flex items-center gap-2">
                        <TrendingUp className="w-4 h-4 text-green-500" />
                        Insights into your productivity and task distribution.
                    </p>
                </div>
                <button
                    onClick={() => router.back()}
                    className="flex items-center gap-2 px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-2xl font-bold shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all hover:-translate-x-1"
                >
                    <ArrowLeft className="w-5 h-5" />
                    Go Back
                </button>
            </div>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                {stats.map((stat, idx) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        className="p-6 bg-white dark:bg-gray-800/50 backdrop-blur-xl rounded-[2rem] border border-gray-100 dark:border-gray-700/50 shadow-sm hover:shadow-xl transition-all group"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className={`p-4 rounded-2xl ${stat.lightColor} ${stat.textColor} group-hover:scale-110 transition-transform`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <span className="text-xs font-black text-gray-400 uppercase tracking-widest">{stat.label}</span>
                        </div>
                        <div className="mt-2">
                            <h3 className="text-3xl font-black text-gray-900 dark:text-white tracking-tight">{stat.value}</h3>
                        </div>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Priority Distribution */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                    className="p-8 bg-white dark:bg-gray-800/50 backdrop-blur-xl rounded-[2.5rem] border border-gray-100 dark:border-gray-700/50 shadow-sm"
                >
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-2xl font-black text-gray-900 dark:text-white">Task Priority</h3>
                            <p className="text-sm text-gray-500 font-medium mt-1">Weightage of tasks by urgency level</p>
                        </div>
                        <AlertCircle className="w-6 h-6 text-gray-400" />
                    </div>

                    <div className="space-y-8">
                        {[
                            { label: "High Priority", count: highPriority, total: totalTasks, color: "bg-red-500", light: "bg-red-100 dark:bg-red-900/30", text: "text-red-600" },
                            { label: "Medium Priority", count: mediumPriority, total: totalTasks, color: "bg-yellow-500", light: "bg-yellow-100 dark:bg-yellow-900/30", text: "text-yellow-600" },
                            { label: "Low Priority", count: lowPriority, total: totalTasks, color: "bg-green-500", light: "bg-green-100 dark:bg-green-900/30", text: "text-green-600" }
                        ].map((item) => {
                            const percent = totalTasks > 0 ? Math.round((item.count / totalTasks) * 100) : 0;
                            return (
                                <div key={item.label} className="space-y-3">
                                    <div className="flex justify-between items-end">
                                        <span className="text-sm font-bold text-gray-700 dark:text-gray-300">{item.label}</span>
                                        <div className="text-right">
                                            <span className="text-lg font-black text-gray-900 dark:text-white">{item.count}</span>
                                            <span className="text-xs text-gray-500 ml-1 font-bold">({percent}%)</span>
                                        </div>
                                    </div>
                                    <div className="h-4 bg-gray-100 dark:bg-gray-700/50 rounded-full overflow-hidden p-1">
                                        <motion.div
                                            initial={{ width: 0 }}
                                            animate={{ width: `${percent}%` }}
                                            transition={{ duration: 1, ease: "easeOut" }}
                                            className={`h-full ${item.color} rounded-full`}
                                        />
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </motion.div>

                {/* Completion Journey */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 }}
                    className="p-8 bg-white dark:bg-gray-800/50 backdrop-blur-xl rounded-[2.5rem] border border-gray-100 dark:border-gray-700/50 shadow-sm flex flex-col justify-center items-center text-center overflow-hidden relative"
                >
                    {/* Background Graphic */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 blur-[100px] rounded-full -mr-32 -mt-32" />
                    <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/5 blur-[100px] rounded-full -ml-32 -mb-32" />

                    <div className="relative z-10">
                        <div className="relative inline-flex mb-8">
                            {/* Circular Progress */}
                            <svg className="w-48 h-48 transform -rotate-90">
                                <circle
                                    cx="96"
                                    cy="96"
                                    r="88"
                                    stroke="currentColor"
                                    strokeWidth="12"
                                    fill="transparent"
                                    className="text-gray-100 dark:text-gray-700"
                                />
                                <motion.circle
                                    cx="96"
                                    cy="96"
                                    r="88"
                                    stroke="currentColor"
                                    strokeWidth="12"
                                    fill="transparent"
                                    strokeDasharray={2 * Math.PI * 88}
                                    initial={{ strokeDashoffset: 2 * Math.PI * 88 }}
                                    animate={{ strokeDashoffset: 2 * Math.PI * 88 * (1 - completionRate / 100) }}
                                    transition={{ duration: 1.5, ease: "easeInOut" }}
                                    strokeLinecap="round"
                                    className="text-blue-600"
                                />
                            </svg>
                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                <span className="text-5xl font-black text-gray-900 dark:text-white">{completionRate}%</span>
                                <span className="text-xs font-bold text-gray-500 uppercase tracking-widest mt-1">Growth</span>
                            </div>
                        </div>

                        <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-2">Overall Completion</h3>
                        <p className="text-gray-500 font-medium max-w-xs mx-auto">
                            You've conquered {completedTasks} out of {totalTasks} objectives. Keep pushing!
                        </p>

                        <div className="mt-8 flex gap-4">
                            <div className="px-5 py-2.5 bg-gray-50 dark:bg-gray-700/50 rounded-2xl border border-gray-100 dark:border-gray-700/50">
                                <span className="block text-[10px] font-black text-gray-400 uppercase tracking-wider mb-1">Goal</span>
                                <span className="block font-bold text-gray-900 dark:text-white">{totalTasks}</span>
                            </div>
                            <div className="px-5 py-2.5 bg-gray-50 dark:bg-gray-700/50 rounded-2xl border border-gray-100 dark:border-gray-700/50">
                                <span className="block text-[10px] font-black text-gray-400 uppercase tracking-wider mb-1">Success</span>
                                <span className="block font-bold text-gray-900 dark:text-white">{completedTasks}</span>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
