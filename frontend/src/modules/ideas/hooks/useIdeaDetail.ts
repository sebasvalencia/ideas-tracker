"use client";

import { useCallback, useEffect, useState } from "react";

import type { Idea } from "@/modules/ideas/model/idea.types";
import { getIdeaById } from "@/modules/ideas/services/ideasApi";

export function useIdeaDetail(token: string | null, ideaId: number | null) {
  const [idea, setIdea] = useState<Idea | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!token || !ideaId) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await getIdeaById(token, ideaId);
      setIdea(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load idea";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [token, ideaId]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return {
    idea,
    loading,
    error,
    refresh,
  };
}
