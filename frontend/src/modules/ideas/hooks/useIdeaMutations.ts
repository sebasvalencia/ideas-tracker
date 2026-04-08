"use client";

import { useState } from "react";

import type { Idea, UpdateIdeaInput } from "@/modules/ideas/model/idea.types";
import { deleteIdea, updateIdea } from "@/modules/ideas/services/ideasApi";

export function useIdeaMutations(token: string | null, ideaId: number | null) {
  const [loading, setLoading] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function patchIdea(payload: UpdateIdeaInput): Promise<Idea | null> {
    if (!token || !ideaId) {
      return null;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await updateIdea(token, ideaId, payload);
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update idea";
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function removeIdea(): Promise<boolean> {
    if (!token || !ideaId) {
      return false;
    }
    setDeleting(true);
    setError(null);
    try {
      await deleteIdea(token, ideaId);
      return true;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete idea";
      setError(message);
      return false;
    } finally {
      setDeleting(false);
    }
  }

  return {
    patchIdea,
    loading,
    deleting,
    removeIdea,
    error,
    clearError: () => setError(null),
  };
}
