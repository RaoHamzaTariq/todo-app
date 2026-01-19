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
  Sun
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const sidebarVariants = {
  open: { x: 0, opacity: 1 },
  closed: { x: -300, opacity: 0 }
};

const navItems = [
  { icon: Home, label: "Dashboard", href: "/dashboard" },
  { icon: CheckSquare, label: "My Tasks", href: "/tasks" },
  { icon: Calendar, label: "Calendar", href: "/calendar" },
  { icon: Star, label: "Important", href: "/important" },
  { icon: Archive, label: "Archive", href: "/archive" },
];

export default function Sidebar({ isOpen, toggleSidebar }: { isOpen: boolean; toggleSidebar: () => void }) {
  const pathname = usePathname();
  const [isMobile, setIsMobile] = useState(false);

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
            className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
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
        className={`fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-white dark:bg-gray-900 shadow-xl z-40 md:relative md:top-0 md:h-screen md:translate-x-0 overflow-y-auto ${
          isMobile ? 'h-[calc(100vh-4rem)]' : ''
        }`}
      >
        <div className="p-6">
          {/* User Profile */}
          <div className="flex items-center space-x-3 mb-8 p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="font-medium text-gray-900 dark:text-white">John Doe</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">john@example.com</p>
            </div>
          </div>

          {/* Quick Actions */}
          <Link href="/tasks/new">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-4 rounded-lg font-medium shadow-lg hover:shadow-xl transition-shadow"
            >
              <Plus className="w-4 h-4" />
              <span>Add New Task</span>
            </motion.button>
          </Link>

          {/* Navigation */}
          <nav className="mt-8 space-y-1">
            {navItems.map((item, index) => {
              const isActive = pathname === item.href;
              return (
                <Link key={item.href} href={item.href}>
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-lg cursor-pointer transition-colors ${
                      isActive
                        ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400"
                        : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                    }`}
                  >
                    <item.icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </motion.div>
                </Link>
              );
            })}
          </nav>

          {/* Filters */}
          <div className="mt-8">
            <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
              Filters
            </h3>
            <div className="space-y-2">
              <button className="flex items-center space-x-2 w-full text-left px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
                <Filter className="w-4 h-4" />
                <span>All Tasks</span>
              </button>
              <button className="flex items-center space-x-2 w-full text-left px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
                <Star className="w-4 h-4" />
                <span>Important</span>
              </button>
              <button className="flex items-center space-x-2 w-full text-left px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
                <Calendar className="w-4 h-4" />
                <span>Due Soon</span>
              </button>
            </div>
          </div>

          {/* Settings */}
          <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
            <Link href="/settings">
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer"
              >
                <Settings className="w-5 h-5" />
                <span className="font-medium">Settings</span>
              </motion.div>
            </Link>
          </div>
        </div>
      </motion.aside>
    </>
  );
}