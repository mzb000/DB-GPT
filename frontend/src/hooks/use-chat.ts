"use client";

import { useState, useCallback, useRef } from "react";
import { api } from "@/lib/api-client";
import type { ChatEvent } from "@/types";

export function useChat() {
  const [events, setEvents] = useState<ChatEvent[]>([]);
  const [streaming, setStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (message: string, datasourceId?: string, modelProvider: string = "ollama") => {
    setStreaming(true);
    setEvents([]);

    try {
      const response = await api.chatStream({ message, datasource_id: datasourceId, model_provider: modelProvider });
      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const data = line.replace(/^data: /, "").trim();
          if (!data || data === "[DONE]") continue;
          try {
            const event: ChatEvent = JSON.parse(data);
            setEvents((prev) => [...prev, event]);
          } catch {}
        }
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Connection error";
      setEvents((prev) => [...prev, { type: "error", content: errorMessage }]);
    } finally {
      setStreaming(false);
    }
  }, []);

  const clear = useCallback(() => setEvents([]), []);

  const stop = useCallback(() => {
    abortRef.current?.abort();
    setStreaming(false);
  }, []);

  return { events, streaming, sendMessage, clear, stop };
}
