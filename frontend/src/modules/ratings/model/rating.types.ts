export type IdeaRating = {
  id: number;
  idea_id: number;
  rating: number;
  summary: string | null;
  created_at: string;
};

export type UpsertIdeaRatingInput = {
  rating: number;
  summary?: string | null;
};
