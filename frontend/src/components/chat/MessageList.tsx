import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Message } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { MessageCircle } from "lucide-react";
import { staggerContainer } from "@/lib/motion-variants";
import { cn } from "@/lib/utils";

interface MessageListProps {
  messages: Message[];
  className?: string;
}

export const MessageList = ({
  messages,
  className = ""
}: MessageListProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }, [messages]);

  return (
    <motion.div
      className={cn("space-y-3 sm:space-y-4 py-2", className)}
      variants={staggerContainer}
      initial="initial"
      animate="animate"
    >
      <AnimatePresence>
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            role={message.role}
            content={message.content}
            timestamp={message.createdAt}
            status={message.status}
          />
        ))}
      </AnimatePresence>

      {messages.length === 0 && (
        <motion.div
          className="flex flex-col items-center justify-center py-12 px-4 text-center"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="w-16 h-16 rounded-full bg-linear-to-br from-blue-100 to-indigo-100 dark:from-blue-900 dark:to-indigo-900 flex items-center justify-center mb-4">
            <MessageCircle className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <p className="text-gray-500 dark:text-gray-400 font-medium">No messages yet</p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">Start a conversation to get help with your tasks</p>
        </motion.div>
      )}

      <div ref={scrollRef} />
    </motion.div>
  );
};