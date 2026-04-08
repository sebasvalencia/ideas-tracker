export type ProgressLog = {
  id: number;
  idea_id: number;
  author_id: number;
  comment: string;
  progress_snapshot: number;
  status_snapshot: string;
  created_at: string;
};

export type CreateProgressLogInput = {
  comment: string;
};
