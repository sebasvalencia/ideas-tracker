"use client";

import { useCallback, useEffect, useState } from "react";

import type { IdeaRating } from "@/modules/ratings/model/rating.types";
import { createIdeaRating, getIdeaRating, updateIdeaRating } from "@/modules/ratings/services/ratingsApi";

export function useIdeaRating(token: string | null, ideaId: number | null, enabled: boolean) {
  const [rating, setRating] = useState<IdeaRating | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!token || !ideaId || !enabled) {
      setRating(null);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await getIdeaRating(token, ideaId);
      setRating(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load rating";
      if (message.toLowerCase().includes("rating not found")) {
        setRating(null);
      } else {
        setError(message);
      }
    } finally {
      setLoading(false);
    }
  }, [enabled, ideaId, token]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function save(payload: { rating: number; summary?: string | null }) {
    if (!token || !ideaId || !enabled) {
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const data = rating
        ? await updateIdeaRating(token, ideaId, payload)
        : await createIdeaRating(token, ideaId, payload);
      setRating(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to save rating";
      setError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return {
    rating,
    loading,
    submitting,
    error,
    save,
    refresh,
  };
}
