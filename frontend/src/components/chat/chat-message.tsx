"use client";

import { useState } from "react";
import type { ChatEvent } from "@/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ResultDisplay } from "./result-display";
import { Loader2, Lightbulb, Database, BarChart3, AlertCircle, CheckCircle2, Copy, Check } from "lucide-react";

interface Props {
  event: ChatEvent;
}

const iconMap: Record<string, React.ReactNode> = {
  status: <Loader2 className="h-4 w-4 animate-spin" />,
  plan: <Lightbulb className="h-4 w-4" />,
  sql: <Database className="h-4 w-4" />,
  result: <BarChart3 className="h-4 w-4" />,
  analysis: <CheckCircle2 className="h-4 w-4" />,
  error: <AlertCircle className="h-4 w-4" />,
  chart: <BarChart3 className="h-4 w-4" />,
};

const colorMap: Record<string, string> = {
  status: "bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800",
  plan: "bg-purple-50 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800",
  sql: "bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800",
  result: "bg-white dark:bg-card",
  analysis: "bg-indigo-50 dark:bg-indigo-950/30 text-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800",
  error: "bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800",
  chart: "bg-white dark:bg-card",
};

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Button variant="ghost" size="sm" onClick={copy} className="h-7 gap-1.5 text-xs">
      {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
      {copied ? "Copied" : "Copy"}
    </Button>
  );
}

export function ChatMessage({ event }: Props) {
  if (event.type === "result") {
    let data;
    try { data = JSON.parse(event.content); } catch { data = null; }
    return (
      <div className="flex justify-start">
        <Card className="max-w-3xl w-full p-4">
          <ResultDisplay columns={data?.columns || []} rows={data?.rows || []} />
        </Card>
      </div>
    );
  }

  if (event.type === "sql") {
    return (
      <div className="flex justify-start">
        <div className="max-w-3xl w-full rounded-lg border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-950/30 p-4">
          <div className="mb-2 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-medium text-green-700 dark:text-green-300">
              <Database className="h-4 w-4" /> Generated SQL
            </div>
            <CopyButton text={event.content} />
          </div>
          <pre className="overflow-x-auto rounded bg-white dark:bg-card p-3 text-sm font-mono">{event.content}</pre>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className={`max-w-3xl rounded-lg border p-4 ${colorMap[event.type] || "bg-white dark:bg-card"}`}>
        <div className="mb-1 flex items-center gap-2 text-sm font-medium">
          {iconMap[event.type]}
          <span className="capitalize">{event.type}</span>
        </div>
        <p className="text-sm whitespace-pre-wrap">{event.content}</p>
      </div>
    </div>
  );
}
