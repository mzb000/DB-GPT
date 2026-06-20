"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { Settings } from "@/types";

export function useSettings() {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<Settings>("/api/v1/settings/")
      .then(setSettings)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const update = useCallback(async (body: Partial<Settings>) => {
    const updated = await api.put<Settings>("/api/v1/settings/", body);
    setSettings(updated);
    return updated;
  }, []);

  return { settings, loading, update };
}
