"use client";

import { motion } from "framer-motion";
import { Archive, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function ArchivePage() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
            <Archive className="w-20 h-20 text-blue-500 mb-8" />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Archive is Coming Soon</h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-lg mb-8">Access your completed and archived tasks here in the future.</p>
            <Link href="/tasks/completed">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                    className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold shadow-lg">
                    View Completed Tasks
                </motion.button>
            </Link>
        </div>
    );
}
