"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Home,
  Calendar,
  CheckSquare,
  Star,
  Archive,
  Settings,
  Plus,
  Search,
  Filter,
  User,
  Bell,
  Moon,
  Sun,
  BarChart3
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { authClient } from "@/lib/auth-client";
const sidebarVariants = {
  open: {
    x: 0,
    opacity: 1,
    width: "18rem", // 72 in tailwind
    transition: { type: "spring" as const, damping: 25, stiffness: 200 }
  },
  closed: {
    x: -300,
    opacity: 0,
    width: 0,
    transition: { type: "spring" as const, damping: 25, stiffness: 200 }
  }
};

const navItems = [
  { icon: Home, label: "Dashboard", href: "/dashboard" },
  { icon: CheckSquare, label: "Tasks", href: "/tasks" },
  { icon: BarChart3, label: "Analytics", href: "/analytics" },
  { icon: Star, label: "Important", href: "/important" },
  { icon: Calendar, label: "Calendar", href: "/calendar" },
  { icon: Archive, label: "Archive", href: "/archive" },
];

export default function Sidebar({ isOpen, toggleSidebar }: { isOpen: boolean; toggleSidebar: () => void }) {
  const pathname = usePathname();
  const [isMobile, setIsMobile] = useState(false);
  const { data: session } = authClient.useSession();

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <>
      {/* Overlay for mobile */}
      <AnimatePresence>
        {isOpen && isMobile && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm"
            onClick={toggleSidebar}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={isOpen ? "open" : "closed"}
        variants={sidebarVariants}
        transition={{ type: "spring", damping: 25, stiffness: 200 }}
        className={`fixed left-0 top-16 h-[calc(100vh-4rem)] w-72 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-r border-gray-200 dark:border-gray-800 shadow-xl z-40 md:relative md:top-0 md:h-screen md:translate-x-0 overflow-hidden flex flex-col`}
      >
        <div className="p-6 flex-1 overflow-y-auto no-scrollbar">
          {/* User Profile */}
          <div className="flex items-center space-x-4 mb-8 p-4 rounded-2xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700/50 group transition-all hover:bg-white dark:hover:bg-gray-800 shadow-sm">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:rotate-6 transition-transform">
              <span className="text-white font-bold text-lg">
                {session?.user?.name?.charAt(0).toUpperCase() || <User className="w-6 h-6" />}
              </span>
            </div>
            <div className="min-w-0 flex-1">
              <p className="font-bold text-gray-900 dark:text-white truncate text-sm">
                {session?.user?.name || "User"}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                {session?.user?.email}
              </p>
            </div>
          </div>

          {/* Quick Actions */}
          <Link href="/tasks/new">
            <motion.button
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              className="w-full flex items-center justify-center space-x-3 bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-4 px-4 rounded-2xl font-bold shadow-xl shadow-blue-600/20 hover:shadow-blue-600/30 transition-all"
            >
              <Plus className="w-5 h-5" />
              <span>Create New Task</span>
            </motion.button>
          </Link>

          {/* Navigation */}
          <nav className="mt-10 space-y-2">
            <p className="px-4 text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] mb-4">
              Main Menu
            </p>
            {navItems.map((item, index) => {
              const isActive = pathname === item.href;
              return (
                <Link key={item.href} href={item.href}>
                  <motion.div
                    whileHover={{ x: 4 }}
                    whileTap={{ scale: 0.98 }}
                    className={`flex items-center space-x-3 px-4 py-3.5 rounded-2xl cursor-pointer transition-all ${isActive
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-600/20"
                      : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white"
                      }`}
                  >
                    <item.icon className={`w-5 h-5 ${isActive ? 'text-white' : ''}`} />
                    <span className="font-bold text-sm tracking-tight">{item.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="activeIndicator"
                        className="ml-auto w-1.5 h-1.5 rounded-full bg-white"
                      />
                    )}
                  </motion.div>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Bottom Actions / Settings */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-800">
          <Link href="/settings">
            <motion.div
              whileHover={{ x: 4 }}
              whileTap={{ scale: 0.98 }}
              className={`flex items-center space-x-3 px-4 py-3.5 rounded-2xl cursor-pointer transition-all ${pathname === '/settings'
                ? "bg-gray-900 dark:bg-white text-white dark:text-gray-900 shadow-lg"
                : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                }`}
            >
              <Settings className="w-5 h-5" />
              <span className="font-bold text-sm tracking-tight">Settings</span>
            </motion.div>
          </Link>
        </div>
      </motion.aside>
    </>
  );
}