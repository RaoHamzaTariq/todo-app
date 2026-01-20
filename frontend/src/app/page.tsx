"use client"
import Link from "next/link";
import { motion } from "framer-motion";
import { CheckCircle, Star, Calendar, Zap } from "lucide-react";

export default function Home() {


  const features = [
    {
      icon: <CheckCircle className="w-8 h-8" />,
      title: "Task Management",
      description: "Organize and track your tasks efficiently"
    },
    {
      icon: <Star className="w-8 h-8" />,
      title: "Priority Setting",
      description: "Set priorities to focus on what matters most"
    },
    {
      icon: <Calendar className="w-8 h-8" />,
      title: "Deadline Tracking",
      description: "Never miss a deadline with our calendar"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Quick Actions",
      description: "Complete tasks with lightning speed"
    }
  ];

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Boost Your <span className="bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Productivity</span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-12">
              StructDo helps you organize, prioritize, and complete your tasks with ease.
              Join thousands of users who have transformed their workflow.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="flex flex-col sm:flex-row justify-center gap-4 mb-16"
          >
            <Link
              href="/sign-in"
              className="px-8 py-4 bg-linear-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-shadow"
            >
              Get Started
            </Link>
            <Link
              href="/sign-up"
              className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-shadow"
            >
              Create Account
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-5xl mx-auto"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 * index }}
                className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className="text-blue-500 dark:text-blue-400 mb-4 flex justify-center">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
