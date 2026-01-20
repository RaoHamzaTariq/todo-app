"use client";

import { useState, useRef, KeyboardEvent, useEffect } from "react";
import { motion } from "framer-motion";
import { Button } from "../ui/Button";
import { cn } from "../../lib/utils";
import { SendHorizonal, Paperclip, Mic } from "lucide-react";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
}

export const MessageInput = ({
  onSend,
  disabled = false,
  placeholder = "Type your message...",
  className = ""
}: MessageInputProps) => {
  const [inputValue, setInputValue] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (inputValue.trim() && !disabled) {
      onSend(inputValue.trim());
      setInputValue("");

      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + "px";
    }
  }, [inputValue]);

  return (
    <div className={cn("flex items-end gap-2 w-full", className)}>
      <motion.div
        className={cn(
          "flex-1 flex items-end border rounded-2xl bg-white/70 dark:bg-gray-800/70",
          "backdrop-blur-sm transition-all duration-200 overflow-hidden",
          isFocused ? "border-blue-500 ring-1 ring-blue-200/50 dark:ring-blue-400/20" : "border-gray-300/50 dark:border-gray-600/50",
          disabled ? "opacity-50 cursor-not-allowed" : ""
        )}
        whileFocus={{ scale: isFocused ? 1.01 : 1 }}
        transition={{ duration: 0.2 }}
      >
        <Button
          variant="ghost"
          size="sm"
          className="m-1.5 h-9 w-9 p-2 rounded-full hover:bg-gray-100/60 dark:hover:bg-gray-700/60 transition-colors"
          disabled={disabled}
        // whileHover={{ scale: 1.1 }}
        // whileTap={{ scale: 0.95 }}
        >
          <Paperclip className="w-4 h-4 text-gray-500 dark:text-gray-400" />
        </Button>

        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          className="flex-1 bg-transparent border-0 focus:outline-none focus:ring-0 resize-none disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] max-h-32 p-3 text-sm placeholder:text-gray-400 dark:placeholder:text-gray-500"
        />

        <div className="flex items-center gap-1 pr-1">
          {inputValue.trim() ? (
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.2 }}
            >
              <Button
                onClick={handleSubmit}
                disabled={!inputValue.trim() || disabled}
                variant="ghost"
                size="sm"
                className="m-1.5 h-9 w-9 p-2 rounded-full hover:bg-blue-100/50 dark:hover:bg-blue-900/30"
              >
                <SendHorizonal className={cn(
                  "h-4 w-4 transition-colors",
                  disabled ? "text-gray-300 dark:text-gray-600" : "text-blue-600 dark:text-blue-400"
                )} />
              </Button>
            </motion.div>
          ) : (
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <Button
                variant="ghost"
                size="sm"
                className="m-1.5 h-9 w-9 p-2 rounded-full hover:bg-gray-100/60 dark:hover:bg-gray-700/60"
                disabled={disabled}
              >
                <Mic className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              </Button>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
};