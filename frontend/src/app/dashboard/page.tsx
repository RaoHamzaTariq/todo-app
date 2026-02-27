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
    TrendingUp,
    Repeat,
    Bell,
    Calendar,
    Tag,
    Filter,
    Search,
    MoreHorizontal
} from "lucide-react";
import { Task } from "@/types/task";
import Link from "next/link";
import { authClient } from "@/lib/auth-client";

// Types for advanced features
type RecurringTask = {
    id: number;
    title: string;
    frequency: string;
    nextOccurrence: Date;
    active: boolean;
};

type Reminder = {
    id: number;
    taskId: number;
    taskTitle: string;
    reminderTime: Date;
    sent: boolean;
};

type TagStat = {
    name: string;
    count: number;
    color: string;
};

export default function DashboardPage() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [recurringTasks, setRecurringTasks] = useState<RecurringTask[]>([]);
    const [reminders, setReminders] = useState<Reminder[]>([]);
    const [loading, setLoading] = useState(true);
    const { data: session } = authClient.useSession();

    useEffect(() => {
        // Fetch all data for dashboard
        Promise.all([
            fetch("/api/tasks").then(res => res.json()),
            fetch("/api/recurring-tasks").then(res => res.json()),
            fetch("/api/reminders").then(res => res.json())
        ]).then(([tasksData, recurringData, remindersData]) => {
            setTasks(Array.isArray(tasksData.tasks) ? tasksData.tasks : tasksData);
            setRecurringTasks(recurringData.recurringTasks || []);
            setReminders(remindersData.reminders || []);
        }).catch(err => {
            console.error("Failed to fetch dashboard data", err);
        }).finally(() => {
            setLoading(false);
        });
    }, []);

    // Calculate stats
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;
    const starred = tasks.filter(t => t.starred).length;
    const recurringActive = recurringTasks.filter(rt => rt.active).length;
    const upcomingReminders = reminders.filter(r => !r.sent).length;
    const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    // Calculate tag statistics
    const tagStats: TagStat[] = [];
    tasks.forEach(task => {
        if (task.tags && Array.isArray(task.tags)) {
            const tags = task.tags.map(tag => tag.trim());
            tags.forEach(tag => {
                const existingTag = tagStats.find(ts => ts.name === tag);
                if (existingTag) {
                    existingTag.count++;
                } else {
                    tagStats.push({
                        name: tag,
                        count: 1,
                        color: getRandomColor()
                    });
                }
            });
        }
    });

    // Helper function to get random colors for tags
    function getRandomColor(): string {
        const colors = [
            'bg-red-100 text-red-800',
            'bg-blue-100 text-blue-800',
            'bg-green-100 text-green-800',
            'bg-yellow-100 text-yellow-800',
            'bg-purple-100 text-purple-800',
            'bg-pink-100 text-pink-800',
            'bg-indigo-100 text-indigo-800',
            'bg-orange-100 text-orange-800',
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    const stats = [
        { label: "Total Load", value: total, icon: BarChart3, color: "text-blue-600", bg: "bg-blue-50 dark:bg-blue-900/20", borderColor: "border-blue-100 dark:border-blue-900/40" },
        { label: "Finished", value: completed, icon: CheckCircle2, color: "text-green-600", bg: "bg-green-50 dark:bg-green-900/20", borderColor: "border-green-100 dark:border-green-900/40" },
        { label: "In Progress", value: pending, icon: Clock, color: "text-yellow-600", bg: "bg-yellow-50 dark:bg-yellow-900/20", borderColor: "border-yellow-100 dark:border-yellow-900/40" },
        { label: "Critical", value: starred, icon: Star, color: "text-purple-600", bg: "bg-purple-50 dark:bg-purple-900/20", borderColor: "border-purple-100 dark:border-purple-900/40" },
        { label: "Recurring", value: recurringActive, icon: Repeat, color: "text-indigo-600", bg: "bg-indigo-50 dark:bg-indigo-900/20", borderColor: "border-indigo-100 dark:border-indigo-900/40" },
        { label: "Reminders", value: upcomingReminders, icon: Bell, color: "text-orange-600", bg: "bg-orange-50 dark:bg-orange-900/20", borderColor: "border-orange-100 dark:border-orange-900/40" },
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

                <div className="flex gap-4">
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

                    <Link href="/tasks/recurring">
                        <motion.button
                            whileHover={{ scale: 1.02, y: -2 }}
                            whileTap={{ scale: 0.98 }}
                            className="flex items-center gap-3 bg-indigo-600 text-white px-6 py-4 rounded-2xl font-black shadow-lg hover:shadow-indigo-500/20 transition-all text-sm"
                        >
                            <Repeat className="w-5 h-5" />
                            Recurring Tasks
                        </motion.button>
                    </Link>
                </div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-12">
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
                                <Zap className="w-5 h-5" />
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
                                        <div className="flex items-center gap-2 mt-1">
                                            {task.due_date && (
                                                <span className="text-[10px] uppercase font-black text-gray-400 tracking-wider flex items-center gap-1">
                                                    <Calendar className="w-3 h-3" /> Due {new Date(task.due_date).toLocaleDateString()}
                                                </span>
                                            )}
                                            <span className="text-[10px] uppercase font-black text-gray-400 tracking-wider">
                                                {task.priority} Priority
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex items-center gap-2">
                                    {task.tags && Array.isArray(task.tags) && task.tags.map((tag, idx) => (
                                        <span key={idx} className={`text-[10px] px-2 py-1 rounded-full ${getRandomColor()}`}>
                                            {tag.trim()}
                                        </span>
                                    ))}

                                    {task.starred && (
                                        <div className="p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded-xl">
                                            <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                        {tasks.filter(t => !t.completed).length === 0 && (
                            <div className="text-center py-12">
                                <p className="text-gray-500 font-bold italic">All objectives completed!</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column: Advanced Features */}
                <div className="flex flex-col gap-8">
                    {/* Upcoming Reminders */}
                    <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-[2rem] border border-gray-100 dark:border-gray-700/50 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <Bell className="w-5 h-5 text-orange-500" />
                                <h3 className="font-black text-gray-900 dark:text-white">Upcoming Reminders</h3>
                            </div>
                            <Link href="/settings/reminders">
                                <MoreHorizontal className="w-4 h-4 text-gray-400 hover:text-gray-600" />
                            </Link>
                        </div>

                        <div className="space-y-3">
                            {reminders.slice(0, 3).map(reminder => (
                                <div key={reminder.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/30 rounded-xl">
                                    <div>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white">{reminder.taskTitle}</p>
                                        <p className="text-xs text-gray-500">{new Date(reminder.reminderTime).toLocaleString()}</p>
                                    </div>
                                    <div className={`w-3 h-3 rounded-full ${reminder.sent ? 'bg-green-500' : 'bg-orange-500'}`} />
                                </div>
                            ))}

                            {reminders.length === 0 && (
                                <p className="text-sm text-gray-500 text-center py-4">No upcoming reminders</p>
                            )}
                        </div>
                    </div>

                    {/* Recurring Tasks */}
                    <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-[2rem] border border-gray-100 dark:border-gray-700/50 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <Repeat className="w-5 h-5 text-indigo-500" />
                                <h3 className="font-black text-gray-900 dark:text-white">Recurring Tasks</h3>
                            </div>
                            <Link href="/tasks/recurring">
                                <MoreHorizontal className="w-4 h-4 text-gray-400 hover:text-gray-600" />
                            </Link>
                        </div>

                        <div className="space-y-3">
                            {recurringTasks.slice(0, 3).map(rt => (
                                <div key={rt.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/30 rounded-xl">
                                    <div>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white">{rt.title}</p>
                                        <p className="text-xs text-gray-500 capitalize">{rt.frequency} • {rt.active ? 'Active' : 'Inactive'}</p>
                                    </div>
                                    <div className={`w-3 h-3 rounded-full ${rt.active ? 'bg-green-500' : 'bg-gray-400'}`} />
                                </div>
                            ))}

                            {recurringTasks.length === 0 && (
                                <p className="text-sm text-gray-500 text-center py-4">No recurring tasks</p>
                            )}
                        </div>
                    </div>

                    {/* Tag Distribution */}
                    <div className="bg-white dark:bg-gray-800/40 backdrop-blur-xl p-6 rounded-[2rem] border border-gray-100 dark:border-gray-700/50 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <Tag className="w-5 h-5 text-purple-500" />
                                <h3 className="font-black text-gray-900 dark:text-white">Popular Tags</h3>
                            </div>
                            <Filter className="w-4 h-4 text-gray-400" />
                        </div>

                        <div className="space-y-2">
                            {tagStats.slice(0, 5).map((tagStat, index) => (
                                <div key={index} className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <span className={`text-[10px] px-2 py-1 rounded-full ${tagStat.color}`}>
                                            {tagStat.name}
                                        </span>
                                    </div>
                                    <span className="text-xs text-gray-500">{tagStat.count}</span>
                                </div>
                            ))}

                            {tagStats.length === 0 && (
                                <p className="text-sm text-gray-500 text-center py-2">No tags available</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Productivity Chart Card */}
            <div className="mt-8 p-8 bg-gradient-to-br from-indigo-600 to-purple-800 rounded-[2.5rem] shadow-2xl shadow-indigo-500/20 text-white relative overflow-hidden group">
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

                    <div className="flex gap-4">
                        <Link href="/analytics">
                            <button className="py-4 bg-white/10 backdrop-blur-md rounded-2xl font-bold text-xs uppercase tracking-widest border border-white/20 hover:bg-white/20 transition-all flex items-center justify-center gap-2 w-full">
                                Insight Details <ArrowRight className="w-4 h-4" />
                            </button>
                        </Link>

                        <Link href="/calendar">
                            <button className="py-4 bg-white/10 backdrop-blur-md rounded-2xl font-bold text-xs uppercase tracking-widest border border-white/20 hover:bg-white/20 transition-all flex items-center justify-center gap-2 w-full">
                                Calendar View <Calendar className="w-4 h-4" />
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}