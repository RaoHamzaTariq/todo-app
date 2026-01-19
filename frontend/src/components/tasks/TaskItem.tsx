import { motion } from "framer-motion";
import { CheckCircle, Circle, Trash2, Edit3, Calendar, Star, AlertCircle } from "lucide-react";
import Link from "next/link";
import { Task } from "@/types/task";

interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 },
  exit: { y: -20, opacity: 0, scale: 0.9 }
};

export default function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  const formattedDate = new Date(task.created_at).toLocaleDateString();

  return (
    <motion.div
      layout
      variants={itemVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      transition={{ duration: 0.3 }}
      className={`p-5 bg-white dark:bg-gray-800 rounded-xl shadow-sm border transition-all hover:shadow-md group ${task.completed
          ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20'
          : 'border-gray-200 dark:border-gray-700'
        }`}
      role="listitem"
      aria-label={`${task.title}${task.completed ? ' (completed)' : ' (incomplete)'}`}
    >
      <div className="flex items-start gap-4">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onToggle}
          className={`mt-0.5 flex-shrink-0 transition-colors ${task.completed ? 'text-green-500 hover:text-green-600' : 'text-gray-400 hover:text-blue-500'
            }`}
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          title={task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.completed ? (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            >
              <CheckCircle className="w-6 h-6" aria-hidden="true" />
            </motion.div>
          ) : (
            <Circle className="w-6 h-6" aria-hidden="true" />
          )}
        </motion.button>

        <div className="flex-1 min-w-0">
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
            <div className="flex-1 min-w-0">
              <motion.h3
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className={`text-lg font-semibold break-words ${task.completed
                    ? 'text-gray-500 dark:text-gray-400 line-through'
                    : 'text-gray-900 dark:text-white'
                  }`}
              >
                {task.title}
              </motion.h3>

              {task.description && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.1 }}
                  className={`mt-2 text-sm ${task.completed
                      ? 'text-gray-400 dark:text-gray-500'
                      : 'text-gray-600 dark:text-gray-300'
                    } break-words`}
                >
                  {task.description}
                </motion.p>
              )}

              {/* Task metadata */}
              <div className="mt-3 flex flex-wrap gap-3 text-xs text-gray-500 dark:text-gray-400">
                <span className="flex items-center gap-1" aria-label={`Created on ${formattedDate}`}>
                  <Calendar className="w-3.5 h-3.5" aria-hidden="true" />
                  {formattedDate}
                </span>

                {task.priority === 'high' && (
                  <span className="flex items-center gap-1 text-red-500">
                    <AlertCircle className="w-3.5 h-3.5" aria-hidden="true" />
                    High Priority
                  </span>
                )}

                {task.starred && (
                  <span className="flex items-center gap-1 text-yellow-500">
                    <Star className="w-3.5 h-3.5" aria-hidden="true" />
                    Important
                  </span>
                )}
              </div>
            </div>

            <div className="flex gap-2 sm:gap-1 flex-shrink-0 mt-1 sm:mt-0">
              <Link href={`/tasks/${task.id}/edit`}>
                <motion.button
                  whileHover={{ scale: 1.1, backgroundColor: "#f3f4f6" }}
                  whileTap={{ scale: 0.9 }}
                  className="p-2 sm:p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  title="Edit task"
                  aria-label="Edit task"
                >
                  <Edit3 className="w-4 h-4 text-gray-600 dark:text-gray-300" aria-hidden="true" />
                  <span className="sr-only">Edit Task</span>
                </motion.button>
              </Link>

              <motion.button
                whileHover={{ scale: 1.1, backgroundColor: "#fee2e2" }}
                whileTap={{ scale: 0.9 }}
                onClick={onDelete}
                className="p-2 sm:p-1.5 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
                title="Delete task"
                aria-label="Delete task"
              >
                <Trash2 className="w-4 h-4 text-red-500" aria-hidden="true" />
                <span className="sr-only">Delete Task</span>
              </motion.button>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}