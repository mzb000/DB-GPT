"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { Dashboard } from "@/types";

export function useDashboards() {
  const [dashboards, setDashboards] = useState<Dashboard[]>([]);
  const [loading, setLoading] = useState(true);

  const fetch = useCallback(async () => {
    try {
      const data = await api.get<Dashboard[]>("/api/v1/dashboards/");
      setDashboards(data);
    } catch {} finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetch(); }, [fetch]);

  const create = useCallback(async (body: { name: string; description?: string }) => {
    const dash = await api.post<Dashboard>("/api/v1/dashboards/", body);
    setDashboards((prev) => [dash, ...prev]);
    return dash;
  }, []);

  const remove = useCallback(async (id: string) => {
    await api.delete(`/api/v1/dashboards/${id}`);
    setDashboards((prev) => prev.filter((d) => d.id !== id));
  }, []);

  return { dashboards, loading, create, remove, refresh: fetch };
}
