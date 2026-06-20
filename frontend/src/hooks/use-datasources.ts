"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { Datasource } from "@/types";

export function useDatasources() {
  const [datasources, setDatasources] = useState<Datasource[]>([]);
  const [loading, setLoading] = useState(true);

  const fetch = useCallback(async () => {
    try {
      const data = await api.get<Datasource[]>("/api/v1/datasources/");
      setDatasources(data);
    } catch {} finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetch(); }, [fetch]);

  const create = useCallback(async (body: { name: string; type: string; config: string; description?: string }) => {
    const ds = await api.post<Datasource>("/api/v1/datasources/", body);
    setDatasources((prev) => [ds, ...prev]);
    return ds;
  }, []);

  const remove = useCallback(async (id: string) => {
    await api.delete(`/api/v1/datasources/${id}`);
    setDatasources((prev) => prev.filter((d) => d.id !== id));
  }, []);

  const testConnection = useCallback(async (type: string, config: Record<string, string>) => {
    return api.post<{ success: boolean; message: string }>("/api/v1/datasources/test-connection", { type, config: JSON.stringify(config) });
  }, []);

  return { datasources, loading, create, remove, testConnection, refresh: fetch };
}
