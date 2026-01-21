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

  // If conversationId is not provided, show a loading state
  if (!conversationId) {
    return (
      <div className={`
        flex flex-col h-full rounded-2xl overflow-hidden
        bg-white/80 backdrop-blur-md
        border border-white/50 shadow-2xl
        dark:bg-gray-900/70 dark:border-white/10
        transition-all duration-300 ease-out
        ${className}
      `}>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mb-4"></div>
            <p>Initializing conversation...</p>
          </div>
        </div>
      </div>
    );
  }

  useEffect(() => {
    const fetchConversationHistory = async () => {
      try {
        // Include proper headers for authentication
        const response = await fetch(`/api/chat/${conversationId}`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.messages && Array.isArray(data.messages)) {
            setMessages(data.messages.map((msg: any) => ({
              id: msg.id,
              role: msg.role,
              content: msg.content,
              createdAt: msg.created_at,
            })));
          }
        } else {
          console.error("Failed to fetch conversation history:", response.statusText);
          // For a new conversation, it's expected that there might be no messages initially
          // Just initialize with an empty array
          setMessages([]);
        }
      } catch (error) {
        console.error("Error fetching conversation history:", error);
        // Initialize with empty array on error
        setMessages([]);
      }
    };

    if (initialMessages.length === 0 && conversationId) {
      fetchConversationHistory();
    } else {
      setMessages(initialMessages);
    }
  }, [userId, conversationId, initialMessages]);

  const handleSendMessage = async (content: string) => {
    if (!conversationId) {
      console.error("Cannot send message: No conversation ID available");
      return;
    }

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
      // Send message to backend API with proper headers
      const response = await fetch(`/api/chat/${conversationId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error sending message:", errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const result = await response.json();

      // Add the AI response to the messages
      const aiMessage: Message = {
        id: result.id || Date.now() + 1,
        role: "assistant",
        content: result.content || "I received your message. How can I help you with your tasks?",
        createdAt: result.created_at || new Date().toISOString(),
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