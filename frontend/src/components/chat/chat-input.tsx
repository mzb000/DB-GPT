"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Send, Trash2 } from "lucide-react";

interface Props {
  onSend: (message: string) => void;
  onClear: () => void;
  disabled: boolean;
}

export function ChatInput({ onSend, onClear, disabled }: Props) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || disabled) return;
    onSend(input.trim());
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t p-4">
      <div className="flex gap-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            e.target.style.height = "auto";
            e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
          }}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your data..."
          className="flex-1 resize-none rounded-md border border-input bg-background px-3 py-2 text-sm outline-none focus:ring-1 focus:ring-ring"
          rows={1}
          disabled={disabled}
        />
        <div className="flex gap-1">
          <Button type="submit" size="icon" disabled={disabled || !input.trim()}>
            <Send className="h-4 w-4" />
          </Button>
          <Button type="button" variant="ghost" size="icon" onClick={onClear} title="Clear chat">
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </form>
  );
}
