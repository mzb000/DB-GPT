"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { Report } from "@/types";

export function useReports() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  const fetch = useCallback(async () => {
    try {
      const data = await api.get<Report[]>("/api/v1/reports/");
      setReports(data);
    } catch {} finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetch(); }, [fetch]);

  const create = useCallback(async (body: { title: string; description?: string; query_ids: string }) => {
    const report = await api.post<Report>("/api/v1/reports/", body);
    setReports((prev) => [report, ...prev]);
    return report;
  }, []);

  const remove = useCallback(async (id: string) => {
    await api.delete(`/api/v1/reports/${id}`);
    setReports((prev) => prev.filter((r) => r.id !== id));
  }, []);

  return { reports, loading, create, remove, refresh: fetch };
}
