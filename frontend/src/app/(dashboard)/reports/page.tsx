"use client";

import { useReports } from "@/hooks/use-reports";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, ExternalLink, Trash2 } from "lucide-react";
import { formatDate } from "@/lib/utils";
import { PageHeader } from "@/components/common/page-header";
import { SkeletonCardGrid } from "@/components/common/skeleton-card";
import { api } from "@/lib/api-client";

export default function ReportsPage() {
  const { reports, loading, remove } = useReports();

  const viewReport = async (id: string) => {
    const html = await api.getReportHtml(id);
    const win = window.open("", "_blank");
    if (win) {
      win.document.write(html);
      win.document.close();
    }
  };

  return (
    <div>
      <PageHeader
        title="Reports"
        description="Shareable HTML analysis reports"
        breadcrumbs={[{ label: "Reports" }]}
      />

      {loading ? (
        <SkeletonCardGrid count={6} />
      ) : reports.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-20">
            <FileText className="h-12 w-12 text-muted-foreground/50" />
            <p className="text-muted-foreground">No reports yet. Generate one from your query results.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {reports.map((report) => (
            <Card key={report.id}>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">{report.title}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground line-clamp-2">{report.description}</p>
                <p className="text-xs text-muted-foreground">{formatDate(report.created_at)}</p>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1" onClick={() => viewReport(report.id)}>
                    <ExternalLink className="mr-1 h-3 w-3" /> View
                  </Button>
                  <Button variant="ghost" size="icon" onClick={() => remove(report.id)}>
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
