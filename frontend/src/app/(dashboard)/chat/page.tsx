"use client";

import { useState } from "react";
import { ChatInterface } from "@/components/chat/chat-interface";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useDatasources } from "@/hooks/use-datasources";
import { MessageSquare, Database, Upload } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { FileUploader } from "@/components/data/file-uploader";

export default function ChatPage() {
  const { datasources, refresh } = useDatasources();
  const [selectedDs, setSelectedDs] = useState<string>("");
  const [modelProvider, setModelProvider] = useState("ollama");

  return (
    <div className="mx-auto flex h-[calc(100vh-100px)] max-w-5xl flex-col">
      <div className="mb-4 flex items-center gap-3">
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
          <SelectTrigger className="w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="gemini">Gemini</SelectItem>
            <SelectItem value="ollama">Ollama</SelectItem>
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
  );
}
