"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
    CheckCircle2,
    Clock,
    Star,
    BarChart3,
    Plus,
    LayoutDashboard,
    ArrowRight,
    Zap,
    TrendingUp
} from "lucide-react";
import { Task } from "@/types/task";
import Link from "next/link";
import { authClient } from "@/lib/auth-client";

export default function DashboardPage() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);
    const { data: session } = authClient.useSession();

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
    const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    const stats = [
        { label: "Total Load", value: total, icon: BarChart3, color: "text-blue-600", bg: "bg-blue-50 dark:bg-blue-900/20", borderColor: "border-blue-100 dark:border-blue-900/40" },
        { label: "Finished", value: completed, icon: CheckCircle2, color: "text-green-600", bg: "bg-green-50 dark:bg-green-900/20", borderColor: "border-green-100 dark:border-green-900/40" },
        { label: "In Progress", value: pending, icon: Clock, color: "text-yellow-600", bg: "bg-yellow-50 dark:bg-yellow-900/20", borderColor: "border-yellow-100 dark:border-yellow-900/40" },
        { label: "Critical", value: starred, icon: Star, color: "text-purple-600", bg: "bg-purple-50 dark:bg-purple-900/20", borderColor: "border-purple-100 dark:border-purple-900/40" },
    ];

    if (loading) return (
        <div className="flex flex-col items-center justify-center min-h-[60vh]">
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"
            />
            <p className="text-gray-500 font-bold">Synchronizing Dashboard...</p>
        </div>
    );

    return (
        <div className="w-full max-w-7xl mx-auto px-4 py-8">
            <header className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                >
                    <p className="text-blue-600 dark:text-blue-400 font-black text-xs uppercase tracking-[0.3em] mb-2">Workspace Overview</p>
                    <h1 className="text-4xl font-black text-gray-900 dark:text-white tracking-tight leading-none">
                        Welcome, {session?.user?.name?.split(' ')[0] || 'User'}!
                    </h1>
                    <p className="text-gray-500 dark:text-gray-400 mt-3 font-medium text-lg">
                        You have <span className="text-blue-600 dark:text-blue-400 font-black">{pending}</span> tasks remaining for today.
                    </p>
                </motion.div>

                <Link href="/tasks/new">
                    <motion.button
                        whileHover={{ scale: 1.02, y: -2 }}
                        whileTap={{ scale: 0.98 }}
                        className="flex items-center gap-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 px-8 py-4 rounded-2xl font-black shadow-2xl hover:shadow-blue-500/20 transition-all text-sm uppercase tracking-widest"
                    >
                        <Plus className="w-5 h-5" />
                        Create New Task
                    </motion.button>
                </Link>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                {stats.map((stat, index) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className={`bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-[2rem] border ${stat.borderColor} shadow-sm group hover:shadow-xl transition-all relative overflow-hidden`}
                    >
                        {/* Decorative Background Icon */}
                        <stat.icon className="absolute -right-4 -bottom-4 w-24 h-24 text-gray-100 dark:text-gray-700/20 rotate-12 group-hover:rotate-0 transition-transform duration-500" />

                        <div className="relative z-10">
                            <div className={`w-12 h-12 rounded-2xl ${stat.bg} ${stat.color} flex items-center justify-center mb-4 shadow-inner group-hover:scale-110 transition-transform`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <h3 className="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest">{stat.label}</h3>
                            <p className="text-3xl font-black text-gray-900 dark:text-white mt-1 tracking-tight">{stat.value}</p>
                        </div>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Recent Tasks List */}
                <div className="lg:col-span-2 bg-white dark:bg-gray-800/40 backdrop-blur-xl p-8 rounded-[2.5rem] border border-gray-100 dark:border-gray-700/50 shadow-sm">
                    <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-blue-500 rounded-xl shadow-lg shadow-blue-500/20">
                                <Zap className="w-5 h-5 text-white" />
                            </div>
                            <h3 className="text-xl font-black text-gray-900 dark:text-white">Active Objectives</h3>
                        </div>
                        <Link href="/tasks">
                            <button className="text-xs font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest hover:translate-x-1 transition-transform flex items-center gap-2">
                                View Full List <ArrowRight className="w-4 h-4" />
                            </button>
                        </Link>
                    </div>

                    <div className="space-y-4">
                        {tasks.filter(t => !t.completed).slice(0, 4).map(task => (
                            <motion.div
                                key={task.id}
                                whileHover={{ x: 10 }}
                                className="flex items-center justify-between p-5 rounded-3xl bg-gray-50/50 dark:bg-gray-900/30 border border-transparent hover:border-blue-500/20 hover:bg-white dark:hover:bg-gray-800 transition-all cursor-pointer group"
                            >
                                <div className="flex items-center gap-4">
                                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${task.priority === 'high' ? 'bg-red-50 dark:bg-red-900/20 text-red-500' : 'bg-blue-50 dark:bg-blue-900/20 text-blue-500'}`}>
                                        <TrendingUp className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <span className="block text-sm font-bold text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">
                                            {task.title}
                                        </span>
                                        <span className="text-[10px] uppercase font-black text-gray-400 tracking-wider">
                                            Due Today • {task.priority} Priority
                                        </span>
                                    </div>
                                </div>
                                {task.starred && (
                                    <div className="p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded-xl">
                                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                    </div>
                                )}
                            </motion.div>
                        ))}
                        {tasks.filter(t => !t.completed).length === 0 && (
                            <div className="text-center py-12">
                                <p className="text-gray-500 font-bold italic">All objectives completed!</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column: Mini Stats Card */}
                <div className="flex flex-col gap-8">
                    {/* Productivity Chart Card */}
                    <div className="p-8 bg-gradient-to-br from-indigo-600 to-purple-800 rounded-[2.5rem] shadow-2xl shadow-indigo-500/20 text-white relative overflow-hidden group">
                        <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-white/10 blur-[80px] rounded-full group-hover:scale-150 transition-transform duration-700" />

                        <div className="relative z-10">
                            <h3 className="text-lg font-black uppercase tracking-widest mb-2 opacity-80">Progress Score</h3>
                            <div className="flex items-end gap-2 mb-6">
                                <span className="text-6xl font-black leading-none">{completionRate}</span>
                                <span className="text-xl font-bold mb-1 opacity-60">%</span>
                            </div>

                            <div className="h-3 w-full bg-white/10 rounded-full mb-8 overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${completionRate}%` }}
                                    transition={{ duration: 1.5, ease: "easeOut" }}
                                    className="h-full bg-white shadow-[0_0_20px_rgba(255,255,255,0.5)]"
                                />
                            </div>

                            <p className="text-sm font-medium leading-relaxed opacity-90 mb-8 font-light">
                                Your journey is evolving. Every completed task brings you closer to your ultimate objective.
                            </p>

                            <Link href="/analytics">
                                <button className="w-full py-4 bg-white/10 backdrop-blur-md rounded-2xl font-bold text-xs uppercase tracking-widest border border-white/20 hover:bg-white/20 transition-all flex items-center justify-center gap-2">
                                    Insight Details <ArrowRight className="w-4 h-4" />
                                </button>
                            </Link>
                        </div>
                    </div>

                    {/* Quick Insight Card */}
                    <Link href="/important" className="group">
                        <div className="p-6 bg-white dark:bg-gray-800/40 backdrop-blur-xl rounded-[2rem] border border-gray-100 dark:border-gray-700/50 shadow-sm flex items-center justify-between group-hover:border-purple-500/50 transition-all">
                            <div className="flex items-center gap-4">
                                <div className="p-4 bg-purple-50 dark:bg-purple-900/20 text-purple-500 rounded-2xl group-hover:rotate-6 transition-transform">
                                    <Star className="w-6 h-6" />
                                </div>
                                <div>
                                    <p className="text-xs font-black text-gray-400 uppercase tracking-widest">Focus List</p>
                                    <p className="text-lg font-black text-gray-900 dark:text-white leading-none mt-1">{starred} Critical Items</p>
                                </div>
                            </div>
                            <ArrowRight className="w-5 h-5 text-gray-300 group-hover:text-purple-500 transition-colors" />
                        </div>
                    </Link>
                </div>
            </div>
        </div>
    );
}
