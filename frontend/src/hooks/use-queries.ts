"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api-client";
import type { QueryResult } from "@/types";

export function useQueries() {
  const [queries, setQueries] = useState<QueryResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<QueryResult[]>("/api/v1/queries/")
      .then(setQueries)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return { queries, loading };
}
