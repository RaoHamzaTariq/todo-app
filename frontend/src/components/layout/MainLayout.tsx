"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu } from "lucide-react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import { FloatingChatWidget } from "../chat/FloatingChatWidget";

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      // Auto-open on desktop, auto-close on mobile ONLY on initial load or resize that crosses threshold
      if (!mobile) {
        setSidebarOpen(true);
      } else {
        setSidebarOpen(false);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col">
      <Header onToggleSidebar={toggleSidebar} isSidebarOpen={sidebarOpen} />

      <div className="flex flex-1 pt-16">
        <Sidebar isOpen={sidebarOpen} toggleSidebar={() => setSidebarOpen(false)} />

        <main className={`flex-1 p-4 md:p-8 bg-gray-50 dark:bg-gray-950 transition-all duration-300 ${sidebarOpen && !isMobile ? "ml-0" : ""}`}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="max-w-7xl mx-auto"
          >
            {children}
          </motion.div>
        </main>
      </div>

      <Footer />

      {/* Floating Chat Widget - appears on all pages */}
      <FloatingChatWidget userId="current-user-id" />

      {/* Mobile menu button - only show if not chat widget */}
      {isMobile && (
        <motion.button
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleSidebar}
          className="fixed bottom-20 right-6 z-40 w-14 h-14 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg flex items-center justify-center"
          aria-label="Open menu"
        >
          <Menu className="w-6 h-6" />
        </motion.button>
      )}
    </div>
  );
}