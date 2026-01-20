"use client";

import { useState, useEffect } from "react";
import { ChatContainer } from "@/components/chat/ChatContainer";
import { Message } from "@/types/chat";

export default function ChatPage() {
  const [userId] = useState<string>("user-123"); // In a real app, this would come from auth
  const [conversationId] = useState<number>(1); // In a real app, this would be dynamic

  // Sample initial messages for demonstration
  const [initialMessages, setInitialMessages] = useState<Message[]>([
    {
      id: 1,
      role: "assistant",
      content: "Hello! I'm your task management assistant. How can I help you today?",
      createdAt: new Date(Date.now() - 300000).toISOString(), // 5 minutes ago
    },
    {
      id: 2,
      role: "user",
      content: "Can you help me create a task to buy groceries?",
      createdAt: new Date(Date.now() - 240000).toISOString(), // 4 minutes ago
    },
    {
      id: 3,
      role: "assistant",
      content: "Sure! I've created a task: 'buy groceries'. Is there anything else you'd like to do?",
      createdAt: new Date(Date.now() - 180000).toISOString(), // 3 minutes ago
    },
  ]);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-bold text-gray-900">AI Task Assistant</h1>
        <p className="text-gray-600 mt-2">Chat with your AI assistant to manage tasks</p>
      </div>

      <div className="h-[600px] border border-gray-200 rounded-xl shadow-sm">
        <ChatContainer
          userId={userId}
          conversationId={conversationId}
          initialMessages={initialMessages}
        />
      </div>

      <div className="mt-6 text-sm text-gray-500 text-center">
        <p>Try asking me to create, list, update, or complete tasks</p>
      </div>
    </div>
  );
}