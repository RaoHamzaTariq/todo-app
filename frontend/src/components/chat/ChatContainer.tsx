"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import { TypingIndicator } from "./TypingIndicator";
import { Message } from "@/types/chat";
import { slideUp } from "@/lib/motion-variants";

interface ChatContainerProps {
  userId: string;
  conversationId: number;
  initialMessages?: Message[];
  className?: string;
}

export const ChatContainer = ({
  userId,
  conversationId,
  initialMessages = [],
  className = ""
}: ChatContainerProps) => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (initialMessages.length === 0) {
      // In a real implementation, fetch conversation history
      // fetch(`/api/${userId}/chat/${conversationId}`)
    }
  }, [userId, conversationId, initialMessages]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content,
      createdAt: new Date().toISOString(),
      status: "sent"
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 1000));

      const aiMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: `I received your message: "${content}". How can I help you with your tasks?`,
        createdAt: new Date().toISOString(),
        status: "delivered"
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: "Sorry, I encountered an error processing your request.",
        createdAt: new Date().toISOString(),
        status: "failed"
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      className={`
        flex flex-col h-full rounded-2xl overflow-hidden
        bg-white/80 backdrop-blur-md 
        border border-white/50 shadow-2xl
        dark:bg-gray-900/70 dark:border-white/10
        transition-all duration-300 ease-out
        ${className}
      `}
      variants={slideUp}
      initial="initial"
      animate="animate"
    >
      <div className="flex-1 overflow-y-auto p-4 pb-2 scroll-smooth">
        <div className="max-w-3xl mx-auto">
          <MessageList messages={messages} />
          <AnimatePresence>
            {isLoading && <TypingIndicator />}
          </AnimatePresence>
        </div>
      </div>

      <div className="border-t border-gray-200/50 dark:border-gray-700/50 p-4 bg-white/60 dark:bg-gray-900/50 backdrop-blur-sm">
        <div className="max-w-3xl mx-auto">
          <MessageInput onSend={handleSendMessage} disabled={isLoading} />
        </div>
      </div>
    </motion.div>
  );
};