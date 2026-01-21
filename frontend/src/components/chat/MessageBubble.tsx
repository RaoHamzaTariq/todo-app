import { useState } from "react";
import { motion } from "framer-motion";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from "../../lib/utils";
import { CheckCheck, Check } from "lucide-react";
import { messageEnter } from "@/lib/motion-variants";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  timestamp: string | Date;
  status?: "sent" | "delivered" | "failed";
  className?: string;
}

export const MessageBubble = ({
  role,
  content,
  timestamp,
  status = "delivered",
  className = "",
}: MessageBubbleProps) => {
  const [isHovered, setIsHovered] = useState(false);
  const isUser = role === "user";

  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);

  const formattedTime = isNaN(date.getTime())
    ? ""
    : date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  return (
    <motion.div
      className={cn(
        "flex",
        isUser ? "justify-end" : "justify-start",
        className
      )}
      variants={messageEnter}
      initial="initial"
      animate="animate"
      exit="exit"
      layout
    >
      <motion.div
        className={cn(
          "max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 shadow-md",
          "backdrop-blur-sm border transition-all duration-200",
          isUser
            ? "bg-linear-to-br from-blue-500 to-indigo-600 text-white border-white/20 rounded-br-none ml-4"
            : "bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-gray-100 border-white/50 dark:border-white/10 rounded-bl-none mr-4"
        )}
        whileHover={{ scale: 1.02 }}
        onHoverStart={() => setIsHovered(true)}
        onHoverEnd={() => setIsHovered(false)}
      >
        <div className="whitespace-pre-wrap wrap-break-word text-sm sm:text-base leading-relaxed">
          <ReactMarkdown
  remarkPlugins={[remarkGfm]}
  components={{
    p: (props) => <p {...props} className="mb-2" />,
    h1: (props) => <h1 {...props} className="text-2xl font-bold mb-3 mt-4" />,
    h2: (props) => <h2 {...props} className="text-xl font-bold mb-2 mt-3" />,
    h3: (props) => <h3 {...props} className="text-lg font-bold mb-2 mt-3" />,
    ul: (props) => <ul {...props} className="list-disc list-inside mb-2 ml-4" />,
    ol: (props) => <ol {...props} className="list-decimal list-inside mb-2 ml-4" />,
    li: (props) => <li {...props} className="mb-1" />,
    strong: (props) => <strong {...props} className="font-semibold" />,
    em: (props) => <em {...props} className="italic" />,
    code: (props) => (
      <code
        {...props}
        className="bg-gray-100 dark:bg-gray-700 px-1 py-0.5 rounded text-sm font-mono"
      />
    ),
    pre: (props) => (
      <pre
        {...props}
        className="bg-gray-100 dark:bg-gray-700 p-3 rounded my-2 overflow-x-auto"
      />
    ),
    blockquote: (props) => (
      <blockquote
        {...props}
        className="border-l-4 border-blue-500 pl-4 italic text-gray-600 dark:text-gray-300"
      />
    ),
    a: (props) => (
      <a
        {...props}
        className="text-blue-600 hover:underline dark:text-blue-400"
        target="_blank"
        rel="noopener noreferrer"
      />
    ),
  }}
>
  {content}
</ReactMarkdown>

        </div>

        <motion.div
          className={cn(
            "text-[11px] mt-1.5 flex items-center justify-end gap-1",
            isUser ? "text-blue-100" : "text-gray-500 dark:text-gray-400"
          )}
          initial={{ opacity: 0 }}
          animate={{ opacity: isHovered ? 0.8 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <span>{formattedTime}</span>
          {isUser && (
            <span className="ml-1">
              <motion.div
                animate={status === "delivered" ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 0.3 }}
              >
                {status === "delivered" ? (
                  <CheckCheck className="w-3 h-3" />
                ) : (
                  <Check className="w-3 h-3" />
                )}
              </motion.div>
            </span>
          )}
        </motion.div>
      </motion.div>
    </motion.div>
  );
};