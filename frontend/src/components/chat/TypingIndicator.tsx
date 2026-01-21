import { motion } from "framer-motion";
import { cn } from "../../lib/utils";
import { dotsPulse } from "@/lib/motion-variants";

interface TypingIndicatorProps {
  className?: string;
}

export const TypingIndicator = ({
  className = ""
}: TypingIndicatorProps) => {
  return (
    <motion.div
      className={cn("flex justify-start py-2", className)}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      <motion.div
        className="
          bg-white/90 dark:bg-gray-800/90 rounded-2xl px-4 py-2 shadow-md 
          border border-white/50 dark:border-white/10 backdrop-blur-sm
        "
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 300 }}
      >
        <div className="flex items-center space-x-1.5">
          {[0, 1, 2].map((index) => (
            <motion.div
              key={index}
              className="w-2 h-2 bg-gradient-to-b from-gray-400 to-gray-500 rounded-full"
              variants={dotsPulse}
              initial="initial"
              animate="animate"
              transition={{ delay: index * 0.2 }}
            />
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
};