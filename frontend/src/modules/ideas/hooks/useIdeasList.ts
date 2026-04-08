"use client";

import { useCallback, useEffect, useState } from "react";

import type { Idea } from "@/modules/ideas/model/idea.types";
import { listIdeas } from "@/modules/ideas/services/ideasApi";

export function useIdeasList(token: string | null) {
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!token) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const rows = await listIdeas(token);
      setIdeas(rows);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load ideas";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return {
    ideas,
    loading,
    error,
    refresh,
  };
}
