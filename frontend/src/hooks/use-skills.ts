"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";
import type { Skill } from "@/types";

export function useSkills() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);

  const fetch = useCallback(async () => {
    try {
      const data = await api.get<Skill[]>("/api/v1/skills/");
      setSkills(data);
    } catch {} finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetch(); }, [fetch]);

  const create = useCallback(async (body: { name: string; description?: string; prompt_template: string; parameters?: string; category?: string }) => {
    const skill = await api.post<Skill>("/api/v1/skills/", body);
    setSkills((prev) => [skill, ...prev]);
    return skill;
  }, []);

  const remove = useCallback(async (id: string) => {
    await api.delete(`/api/v1/skills/${id}`);
    setSkills((prev) => prev.filter((s) => s.id !== id));
  }, []);

  const execute = useCallback(async (skillId: string, datasourceId: string, params: Record<string, string>) => {
    return api.post<{ query_id: string; columns: string[]; rows: unknown[][] }>(`/api/v1/skills/${skillId}/execute`, {
      datasource_id: datasourceId,
      parameter_values: JSON.stringify(params),
    });
  }, []);

  return { skills, loading, create, remove, execute, refresh: fetch };
}
