"use client";

import { motion } from "framer-motion";
import { Hammer, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function ComingSoonPage() {
    const pathname = usePathname();
    const pageName = pathname.substring(1).charAt(0).toUpperCase() + pathname.substring(2);

    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
            <motion.div
                initial={{ rotate: -10 }}
                animate={{ rotate: 10 }}
                transition={{ repeat: Infinity, duration: 1, repeatType: "reverse", ease: "easeInOut" }}
                className="mb-8"
            >
                <Hammer className="w-20 h-20 text-blue-500" />
            </motion.div>

            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                {pageName} is Under Construction
            </h1>

            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-lg mb-8">
                We're working hard to bring you the best experience. The {pageName} feature will be available soon!
            </p>

            <Link href="/dashboard">
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold shadow-lg"
                >
                    <ArrowLeft className="w-5 h-5" />
                    Back to Dashboard
                </motion.button>
            </Link>
        </div>
    );
}
