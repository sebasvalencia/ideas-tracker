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
  const [ratingValue, setRatingValue] = useState<number>(currentRating?.rating ?? 0);
  const [hovered, setHovered] = useState<number>(0);
  const [summary, setSummary] = useState<string>(currentRating?.summary ?? "");
  const [error, setError] = useState<string | null>(null);

  if (!enabled) {
    return (
      <p className={styles.hint}>
        Rating is available only when the idea status is completed.
      </p>
    );
  }

  const displayValue = hovered || ratingValue;

  return (
    <form
      className={styles.form}
      onSubmit={async (event) => {
        event.preventDefault();
        if (ratingValue < 1 || ratingValue > 10) {
          setError("Select a rating between 1 and 10");
          return;
        }
        setError(null);
        await onSubmit({ rating: ratingValue, summary: summary.trim() || null });
      }}
    >
      <div className={styles.row}>
        <label className={styles.label}>Rating</label>
        <div className={styles.starsRow}>
          {Array.from({ length: 10 }, (_, i) => i + 1).map((star) => (
            <button
              aria-label={`Rate ${star} out of 10`}
              className={`${styles.star} ${star <= displayValue ? styles.starFilled : styles.starEmpty}`}
              key={star}
              onClick={() => setRatingValue(star)}
              onMouseEnter={() => setHovered(star)}
              onMouseLeave={() => setHovered(0)}
              type="button"
            >
              ★
            </button>
          ))}
          <span className={styles.ratingNumber}>
            {ratingValue > 0 ? `${ratingValue}/10` : "—"}
          </span>
        </div>
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
