"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "../ui/Button";
import { ChatContainer } from "./ChatContainer";
import { Message } from "@/types/chat";
import { cn } from "../../lib/utils";
import { MessageCircle, X } from "lucide-react";
import { scaleIn, slideUp, pulseRing, fadeIn } from "@/lib/motion-variants";

interface FloatingChatWidgetProps {
  userId: string;
  className?: string;
}

export const FloatingChatWidget = ({ userId, className = "" }: FloatingChatWidgetProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [initialMessages, setInitialMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  // Function to create a new conversation
  const createNewConversation = async () => {
    setLoading(true);
    try {
      // Create conversation with timeout handling
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 1-minute timeout for conversation creation

      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        const data = await response.json();
        setConversationId(data.id);
        return data.id;
      } else {
        console.error('Failed to create conversation:', await response.text());
        // Show error to user and prevent further operations
        alert('Failed to initialize chat. Please refresh the page and try again.');
        setLoading(false);
        return null;
      }
    } catch (error: any) {
      console.error('Error creating conversation:', error);
      let errorMessage = 'Network error occurred while initializing chat. Please check your connection and try again.';

      // Check if it's a timeout error
      if (error.name === 'AbortError') {
        errorMessage = 'Creating conversation timed out. Please try again.';
      } else if (error.message?.includes('timeout')) {
        errorMessage = 'Creating conversation timed out. Please try again.';
      }

      alert(errorMessage);
      setLoading(false);
      return null;
    }
  };

  // Initialize conversation when widget opens
  useEffect(() => {
    if (isOpen && !conversationId) {
      createNewConversation();
    }
  }, [isOpen, conversationId]);


  return (
    <>
      <AnimatePresence>
        {!isOpen && (
          <motion.div
            className="fixed bottom-8 right-8 z-50"
            variants={fadeIn}
            initial="initial"
            animate="animate"
            exit="exit"
          >
            <motion.div
              className={cn(
                "relative",
                hasUnread && "animate-pulse"
              )}
              animate={hasUnread ? "animate" : ""}
              variants={hasUnread ? pulseRing : {}}
            >
              <Button
                onClick={() => {
                  setIsOpen(true);
                  setHasUnread(false);
                }}
                className={cn(
                  "rounded-full w-16 h-16 shadow-lg flex items-center justify-center",
                  "bg-gradient-to-br from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700",
                  "text-white transition-all duration-300 ease-out hover:scale-110 hover:rotate-6",
                  "backdrop-blur-sm border border-white/20",
                  hasUnread && "ring-4 ring-blue-300/40"
                )}
                aria-label="Open chat"
              >
                <motion.div
                  animate={{ rotate: hasUnread ? [0, 12, -12, 0] : 0 }}
                  transition={{ duration: 1, repeat: hasUnread ? Infinity : 0 }}
                >
                  <MessageCircle className="w-7 h-7" />
                </motion.div>
                {hasUnread && (
                  <motion.span
                    className="absolute -top-1 -right-1 flex h-5 w-5"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 500, delay: 0.1 }}
                  >
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-5 w-5 bg-red-500"></span>
                  </motion.span>
                )}
              </Button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-8 right-8 z-50 w-full max-w-md h-[620px] flex flex-col"
            variants={scaleIn}
            initial="initial"
            animate="animate"
            exit="exit"
            style={{ originX: 1, originY: 1 }}
          >
            <div className="
              bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 
              dark:bg-gray-900/80 dark:border-white/10
              flex flex-col h-full overflow-hidden
            ">
              <div className="
                flex justify-between items-center p-5 border-b border-gray-200/50 dark:border-gray-700/50 
                bg-white/70 dark:bg-gray-900/70 backdrop-blur-sm rounded-t-3xl
              ">
                <motion.div
                  className="flex items-center space-x-3"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  <div className="relative">
                    <div className="w-4 h-4 bg-green-500 rounded-full"></div>
                    <div className="absolute inset-0 w-4 h-4 bg-green-400 rounded-full animate-ping opacity-60"></div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Task Assistant</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400">AI-powered help</p>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <Button
                    onClick={() => setIsOpen(false)}
                    variant="ghost"
                    size="sm"
                    className="
                      p-2 h-auto rounded-full hover:bg-gray-100/60 dark:hover:bg-gray-800/60 
                      transition-all duration-200 hover:rotate-90
                    "
                  >
                    <X className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                  </Button>
                </motion.div>
              </div>

              <div className="flex-1 overflow-hidden p-1">
                {conversationId ? (
                  <ChatContainer
                    userId={userId}
                    conversationId={conversationId}
                    initialMessages={initialMessages}
                    className="h-full rounded-xl"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center text-gray-500">
                      <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mb-4"></div>
                      <p>Setting up chat...</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};