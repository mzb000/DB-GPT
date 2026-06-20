"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api-client";

export default function ReportDetail() {
  const { id } = useParams();
  const [html, setHtml] = useState("");

  useEffect(() => {
    api.getReportHtml(id as string).then(setHtml);
  }, [id]);

  return (
    <div className="h-[calc(100vh-100px)]">
      {html ? (
        <iframe className="h-full w-full rounded-lg border" srcDoc={html} title="Report" />
      ) : (
        <div className="py-20 text-center text-muted-foreground">Loading...</div>
      )}
    </div>
  );
}
