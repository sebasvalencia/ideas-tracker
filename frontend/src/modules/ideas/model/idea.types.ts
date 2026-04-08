export type Idea = {
  id: number;
  owner_id: number;
  title: string;
  description: string;
  status: string;
  execution_percentage: number;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
};

export type CreateIdeaInput = {
  title: string;
  description: string;
};

export type UpdateIdeaInput = {
  title?: string;
  description?: string;
  status?: "idea" | "in_progress" | "completed";
  execution_percentage?: number;
};
