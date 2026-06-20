"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api-client";
import { Upload, FileSpreadsheet, CheckCircle2, XCircle } from "lucide-react";

interface Props {
  onDone: () => void;
}

export function FileUploader({ onDone }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{ name: string; rows: number; columns: string[] } | null>(null);
  const [error, setError] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");
    try {
      const res = await api.upload<{ name: string; rows: number; columns: string[] }>("/api/v1/uploads/", file);
      setResult(res);
      setTimeout(onDone, 2000);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div
        className="flex cursor-pointer flex-col items-center gap-2 rounded-lg border-2 border-dashed p-8 hover:border-primary/50"
        onClick={() => inputRef.current?.click()}
      >
        <FileSpreadsheet className="h-10 w-10 text-muted-foreground" />
        <p className="text-sm font-medium">{file ? file.name : "Click to select CSV or Excel file"}</p>
        <p className="text-xs text-muted-foreground">.csv, .xlsx, .xls</p>
        <input
          ref={inputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          className="hidden"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </div>

      {file && !result && (
        <Button onClick={handleUpload} disabled={uploading} className="w-full">
          {uploading ? "Uploading..." : "Upload"}
          <Upload className="ml-2 h-4 w-4" />
        </Button>
      )}

      {error && (
        <div className="flex items-center gap-2 text-sm text-destructive">
          <XCircle className="h-4 w-4" /> {error}
        </div>
      )}

      {result && (
        <div className="flex items-center gap-2 rounded-md bg-green-50 p-3 text-sm text-green-700">
          <CheckCircle2 className="h-4 w-4" />
          Uploaded {result.name} ({result.rows} rows, {result.columns.length} columns)
        </div>
      )}
    </div>
  );
}
