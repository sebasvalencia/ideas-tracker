"use client";

import { useCallback, useEffect, useState } from "react";

import type { ProgressLog } from "@/modules/progress-logs/model/progressLog.types";
import { createProgressLog, listProgressLogs } from "@/modules/progress-logs/services/progressLogsApi";

export function useProgressLogs(token: string | null, ideaId: number | null) {
  const [logs, setLogs] = useState<ProgressLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!token || !ideaId) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await listProgressLogs(token, ideaId);
      setLogs(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load logs";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [ideaId, token]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function addLog(comment: string) {
    if (!token || !ideaId) {
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      await createProgressLog(token, ideaId, { comment });
      await refresh();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to add log";
      setError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return {
    logs,
    loading,
    submitting,
    error,
    addLog,
    refresh,
  };
}
