import type { CreateProgressLogInput, ProgressLog } from "@/modules/progress-logs/model/progressLog.types";
import { requestJson } from "@/shared/lib/apiClient";

export async function listProgressLogs(token: string, ideaId: number): Promise<ProgressLog[]> {
  return requestJson<ProgressLog[]>(`/api/ideas/${ideaId}/logs`, {
    token,
  });
}

export async function createProgressLog(
  token: string,
  ideaId: number,
  payload: CreateProgressLogInput,
): Promise<ProgressLog> {
  return requestJson<ProgressLog>(`/api/ideas/${ideaId}/logs`, {
    method: "POST",
    token,
    body: payload,
  });
}
