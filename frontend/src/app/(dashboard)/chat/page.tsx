"use client";

import { useState, useEffect } from "react";
import { ChatInterface } from "@/components/chat/chat-interface";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useDatasources } from "@/hooks/use-datasources";
import { MessageSquare, Database, Upload, Plus, Trash2, Sparkles, Server } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { FileUploader } from "@/components/data/file-uploader";
import { cn } from "@/lib/utils";

interface Conversation {
  id: string;
  title: string;
  timestamp: number;
}

function loadConversations(): Conversation[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem("chat-conversations") || "[]");
  } catch {
    return [];
  }
}

function saveConversations(convos: Conversation[]) {
  localStorage.setItem("chat-conversations", JSON.stringify(convos));
}

export default function ChatPage() {
  const { datasources, refresh } = useDatasources();
  const [selectedDs, setSelectedDs] = useState<string>("");
  const [modelProvider, setModelProvider] = useState("gemini");
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvo, setActiveConvo] = useState<string | null>(null);

  useEffect(() => {
    setConversations(loadConversations());
  }, []);

  const createConversation = () => {
    const convo: Conversation = {
      id: crypto.randomUUID(),
      title: "New Chat",
      timestamp: Date.now(),
    };
    const updated = [convo, ...conversations];
    setConversations(updated);
    saveConversations(updated);
    setActiveConvo(convo.id);
  };

  const deleteConversation = (id: string) => {
    const updated = conversations.filter((c) => c.id !== id);
    setConversations(updated);
    saveConversations(updated);
    if (activeConvo === id) setActiveConvo(null);
  };

  return (
    <div className="flex h-[calc(100vh-100px)] gap-4">
      <div className="flex w-60 shrink-0 flex-col rounded-lg border bg-card">
        <div className="border-b p-3">
          <Button onClick={createConversation} className="w-full gap-2" size="sm">
            <Plus className="h-3.5 w-3.5" /> New Chat
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          {conversations.length === 0 ? (
            <div className="py-8 text-center text-xs text-muted-foreground">
              No conversations yet
            </div>
          ) : (
            <div className="space-y-1">
              {conversations.map((convo) => (
                <div
                  key={convo.id}
                  className={cn(
                    "group flex items-center gap-2 rounded-md px-2.5 py-2 text-sm cursor-pointer transition-colors",
                    activeConvo === convo.id
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-accent"
                  )}
                  onClick={() => setActiveConvo(convo.id)}
                >
                  <MessageSquare className="h-3.5 w-3.5 shrink-0" />
                  <span className="flex-1 truncate">{convo.title}</span>
                  <button
                    onClick={(e) => { e.stopPropagation(); deleteConversation(convo.id); }}
                    className="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <Trash2 className="h-3 w-3 text-muted-foreground hover:text-destructive" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="flex flex-1 flex-col">
        <div className="mb-3 flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Database className="h-4 w-4 text-muted-foreground" />
            <Select value={selectedDs} onValueChange={setSelectedDs}>
              <SelectTrigger className="w-56">
                <SelectValue placeholder="Select data source..." />
              </SelectTrigger>
              <SelectContent>
                {datasources.map((ds) => (
                  <SelectItem key={ds.id} value={ds.id}>{ds.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <Select value={modelProvider} onValueChange={setModelProvider}>
            <SelectTrigger className="w-44">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="gemini">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-3.5 w-3.5 text-blue-500" />
                  <div>
                    <span className="font-medium">Gemini</span>
                    <span className="ml-1.5 text-xs text-muted-foreground">Cloud AI</span>
                  </div>
                </div>
              </SelectItem>
              <SelectItem value="ollama">
                <div className="flex items-center gap-2">
                  <Server className="h-3.5 w-3.5 text-green-500" />
                  <div>
                    <span className="font-medium">Ollama</span>
                    <span className="ml-1.5 text-xs text-muted-foreground">Local</span>
                  </div>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" size="sm">
                <Upload className="mr-1 h-4 w-4" /> Upload
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Upload CSV or Excel</DialogTitle>
              </DialogHeader>
              <FileUploader onDone={() => { refresh(); }} />
            </DialogContent>
          </Dialog>
        </div>
        <Card className="flex-1">
          <CardContent className="flex h-full flex-col p-0">
            <ChatInterface
              selectedDatasourceId={selectedDs}
              modelProvider={modelProvider}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
