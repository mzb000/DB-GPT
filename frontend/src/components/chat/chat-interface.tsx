"use client";

import { useRef, useEffect } from "react";
import { useChat } from "@/hooks/use-chat";
import { ChatMessage } from "./chat-message";
import { ChatInput } from "./chat-input";

interface Props {
  selectedDatasourceId?: string;
  modelProvider?: string;
}

export function ChatInterface({ selectedDatasourceId, modelProvider = "ollama" }: Props) {
  const { events, streaming, sendMessage, clear } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events]);

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {events.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="mb-4 rounded-full bg-primary/10 p-4">
              <svg className="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Ask anything about your data</h3>
            <p className="mt-1 text-sm text-muted-foreground max-w-md">
              Try "Show me total sales by region" or "What were the top 10 products last quarter?"
            </p>
          </div>
        )}
        {events.map((event, i) => (
          <ChatMessage key={i} event={event} />
        ))}
        <div ref={bottomRef} />
      </div>
      <ChatInput onSend={(msg) => sendMessage(msg, selectedDatasourceId, modelProvider)} disabled={streaming} onClear={clear} />
    </div>
  );
}
