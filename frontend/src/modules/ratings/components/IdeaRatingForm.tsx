"use client";

import { useState } from "react";

import type { IdeaRating } from "@/modules/ratings/model/rating.types";
import styles from "@/modules/ratings/components/IdeaRatingForm.module.scss";

type IdeaRatingFormProps = {
  enabled: boolean;
  loading: boolean;
  currentRating: IdeaRating | null;
  onSubmit: (payload: { rating: number; summary?: string | null }) => Promise<void>;
};

export function IdeaRatingForm({ enabled, loading, currentRating, onSubmit }: IdeaRatingFormProps) {
  const [ratingValue, setRatingValue] = useState<number>(currentRating?.rating ?? 7);
  const [summary, setSummary] = useState<string>(currentRating?.summary ?? "");
  const [error, setError] = useState<string | null>(null);

  if (!enabled) {
    return <p className={styles.hint}>Rating is available only when the idea status is completed.</p>;
  }

  return (
    <form
      className={styles.form}
      onSubmit={async (event) => {
        event.preventDefault();
        if (ratingValue < 1 || ratingValue > 10) {
          setError("Rating must be between 1 and 10");
          return;
        }
        setError(null);
        await onSubmit({
          rating: ratingValue,
          summary: summary.trim() || null,
        });
      }}
    >
      <div className={styles.row}>
        <label className={styles.label} htmlFor="idea-rating">
          Rating (1..10)
        </label>
        <input
          className={styles.input}
          id="idea-rating"
          max={10}
          min={1}
          onChange={(event) => setRatingValue(Number(event.target.value))}
          type="number"
          value={ratingValue}
        />
      </div>

      <div className={styles.row}>
        <label className={styles.label} htmlFor="idea-rating-summary">
          Summary
        </label>
        <textarea
          className={`${styles.input} ${styles.textarea}`}
          id="idea-rating-summary"
          onChange={(event) => setSummary(event.target.value)}
          placeholder="How did this idea end?"
          value={summary}
        />
      </div>

      {error && <p className={styles.error}>{error}</p>}

      <button className={styles.button} disabled={loading} type="submit">
        {loading ? "Saving..." : currentRating ? "Update rating" : "Save rating"}
      </button>
    </form>
  );
}
