"use client";

import { useQueries } from "@/hooks/use-queries";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { History, Clock } from "lucide-react";
import { formatDate, truncate } from "@/lib/utils";
import { PageHeader } from "@/components/common/page-header";
import { SkeletonTable } from "@/components/common/skeleton-table";
import Link from "next/link";

export default function QueriesPage() {
  const { queries, loading } = useQueries();

  return (
    <div>
      <PageHeader
        title="Query History"
        description="Recently executed queries"
        breadcrumbs={[{ label: "Query History" }]}
      />

      {loading ? (
        <SkeletonTable rows={5} />
      ) : queries.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-20">
            <History className="h-12 w-12 text-muted-foreground/50" />
            <p className="text-muted-foreground">No queries yet. Ask a question in the chat.</p>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-base">Recent Queries</CardTitle></CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Question</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Time</TableHead>
                  <TableHead>Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {queries.map((q) => (
                  <TableRow key={q.id}>
                    <TableCell className="font-medium max-w-md">
                      <Link href={`/queries/${q.id}`} className="hover:text-primary transition-colors">
                        {truncate(q.question, 80)}
                      </Link>
                    </TableCell>
                    <TableCell>
                      <Badge variant={q.status === "completed" ? "success" : "warning"}>
                        {q.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" /> {q.execution_time.toFixed(2)}s
                      </span>
                    </TableCell>
                    <TableCell className="text-muted-foreground text-sm">{formatDate(q.created_at)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
