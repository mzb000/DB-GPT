"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api-client";
import { PageHeader } from "@/components/common/page-header";
import { ResultDisplay } from "@/components/chat/result-display";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Clock, Database, Copy, Check, MessageSquare } from "lucide-react";
import { formatDate } from "@/lib/utils";
import type { QueryResult } from "@/types";
import Link from "next/link";

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
      {copied ? "Copied" : "Copy SQL"}
    </Button>
  );
}

export default function QueryDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [query, setQuery] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params.id) {
      api.get<QueryResult>(`/api/v1/queries/${params.id}`)
        .then(setQuery)
        .catch(() => router.push("/queries"))
        .finally(() => setLoading(false));
    }
  }, [params.id, router]);

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="h-8 w-64 animate-pulse rounded bg-muted" />
        <div className="h-40 animate-pulse rounded bg-muted" />
      </div>
    );
  }

  if (!query) return null;

  let resultData: { columns: string[]; rows: unknown[][] } | null = null;
  try {
    resultData = JSON.parse(query.result_json);
  } catch {
    resultData = null;
  }

  return (
    <div>
      <PageHeader
        title={query.question}
        breadcrumbs={[
          { label: "Query History", href: "/queries" },
          { label: `Query` },
        ]}
        actions={
          <Link href={`/chat`}>
            <Button variant="outline" size="sm" className="gap-1.5">
              <MessageSquare className="h-3.5 w-3.5" /> Ask Again
            </Button>
          </Link>
        }
      />

      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          <Badge variant={query.status === "completed" ? "success" : "warning"}>
            {query.status}
          </Badge>
          <span className="flex items-center gap-1 text-sm text-muted-foreground">
            <Clock className="h-3.5 w-3.5" /> {query.execution_time.toFixed(2)}s
          </span>
          <span className="text-sm text-muted-foreground">
            {formatDate(query.created_at)}
          </span>
        </div>

        {query.sql_generated && (
          <Card>
            <CardContent className="pt-4">
              <div className="mb-2 flex items-center justify-between">
                <div className="flex items-center gap-2 text-sm font-medium">
                  <Database className="h-4 w-4 text-green-600" /> Generated SQL
                </div>
                <CopyButton text={query.sql_generated} />
              </div>
              <pre className="overflow-x-auto rounded-md bg-muted p-3 text-sm font-mono">
                {query.sql_generated}
              </pre>
            </CardContent>
          </Card>
        )}

        {query.summary && (
          <Card>
            <CardContent className="pt-4">
              <h3 className="mb-2 text-sm font-medium">Analysis Summary</h3>
              <p className="text-sm text-muted-foreground whitespace-pre-wrap">{query.summary}</p>
            </CardContent>
          </Card>
        )}

        {resultData && resultData.columns && resultData.rows && (
          <Card>
            <CardContent className="pt-4">
              <ResultDisplay columns={resultData.columns} rows={resultData.rows} />
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
