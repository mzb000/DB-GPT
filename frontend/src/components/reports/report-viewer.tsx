"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";

interface Props {
  reportId: string;
}

export function ReportViewer({ reportId }: Props) {
  const [html, setHtml] = useState("");

  useEffect(() => {
    api.getReportHtml(reportId).then(setHtml);
  }, [reportId]);

  if (!html) return <div className="py-20 text-center text-muted-foreground">Loading report...</div>;

  return (
    <iframe className="h-full w-full rounded-lg border" srcDoc={html} title="Report" />
  );
}
