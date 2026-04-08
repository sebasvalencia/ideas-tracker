import type { IdeaRating, UpsertIdeaRatingInput } from "@/modules/ratings/model/rating.types";
import { requestJson } from "@/shared/lib/apiClient";

export async function getIdeaRating(token: string, ideaId: number): Promise<IdeaRating> {
  return requestJson<IdeaRating>(`/api/ideas/${ideaId}/rating`, {
    token,
  });
}

export async function createIdeaRating(token: string, ideaId: number, payload: UpsertIdeaRatingInput): Promise<IdeaRating> {
  return requestJson<IdeaRating>(`/api/ideas/${ideaId}/rating`, {
    method: "POST",
    token,
    body: payload,
  });
}

export async function updateIdeaRating(token: string, ideaId: number, payload: UpsertIdeaRatingInput): Promise<IdeaRating> {
  return requestJson<IdeaRating>(`/api/ideas/${ideaId}/rating`, {
    method: "PATCH",
    token,
    body: payload,
  });
}
