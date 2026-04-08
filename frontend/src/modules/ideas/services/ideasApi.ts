import type { CreateIdeaInput, Idea, UpdateIdeaInput } from "@/modules/ideas/model/idea.types";
import { requestJson } from "@/shared/lib/apiClient";

export async function listIdeas(token: string): Promise<Idea[]> {
  return requestJson<Idea[]>("/api/ideas", {
    token,
  });
}

export async function createIdea(token: string, payload: CreateIdeaInput): Promise<Idea> {
  return requestJson<Idea>("/api/ideas", {
    method: "POST",
    token,
    body: payload,
  });
}

export async function getIdeaById(token: string, ideaId: number): Promise<Idea> {
  return requestJson<Idea>(`/api/ideas/${ideaId}`, {
    token,
  });
}

export async function updateIdea(token: string, ideaId: number, payload: UpdateIdeaInput): Promise<Idea> {
  return requestJson<Idea>(`/api/ideas/${ideaId}`, {
    method: "PATCH",
    token,
    body: payload,
  });
}

export async function deleteIdea(token: string, ideaId: number): Promise<void> {
  await requestJson<void>(`/api/ideas/${ideaId}`, {
    method: "DELETE",
    token,
  });
}
