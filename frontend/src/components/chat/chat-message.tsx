"use client";

import type { ChatEvent } from "@/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ResultDisplay } from "./result-display";
import { Loader2, Lightbulb, Database, Code, BarChart3, AlertCircle, CheckCircle2 } from "lucide-react";

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
  status: "bg-blue-50 text-blue-700 border-blue-200",
  plan: "bg-purple-50 text-purple-700 border-purple-200",
  sql: "bg-green-50 text-green-700 border-green-200",
  result: "bg-white",
  analysis: "bg-indigo-50 text-indigo-700 border-indigo-200",
  error: "bg-red-50 text-red-700 border-red-200",
  chart: "bg-white",
};

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
        <div className="max-w-3xl w-full rounded-lg border border-green-200 bg-green-50 p-4">
          <div className="mb-2 flex items-center gap-2 text-sm font-medium text-green-700">
            <Database className="h-4 w-4" /> Generated SQL
          </div>
          <pre className="overflow-x-auto rounded bg-white p-3 text-sm">{event.content}</pre>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className={`max-w-3xl rounded-lg border p-4 ${colorMap[event.type] || "bg-white"}`}>
        <div className="mb-1 flex items-center gap-2 text-sm font-medium">
          {iconMap[event.type]}
          <span className="capitalize">{event.type}</span>
        </div>
        <p className="text-sm whitespace-pre-wrap">{event.content}</p>
      </div>
    </div>
  );
}
