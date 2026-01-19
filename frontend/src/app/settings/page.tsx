"use client";

import { motion } from "framer-motion";
import { Settings, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function SettingsPage() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
            <Settings className="w-20 h-20 text-gray-500 mb-8" />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Settings</h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-lg mb-8">Customize your experience. This feature is coming soon!</p>
            <Link href="/dashboard">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                    className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold shadow-lg">
                    <ArrowLeft className="w-5 h-5" /> Back to Dashboard
                </motion.button>
            </Link>
        </div>
    );
}
