"use client";

import { useState } from "react";

import styles from "@/modules/progress-logs/components/ProgressLogTextarea.module.scss";

type ProgressLogTextareaProps = {
  loading: boolean;
  onSubmit: (comment: string) => Promise<void>;
};

export function ProgressLogTextarea({ loading, onSubmit }: ProgressLogTextareaProps) {
  const [comment, setComment] = useState("");
  const [error, setError] = useState<string | null>(null);

  return (
    <form
      className={styles.form}
      onSubmit={async (event) => {
        event.preventDefault();
        if (!comment.trim()) {
          setError("Comment is required");
          return;
        }
        setError(null);
        await onSubmit(comment.trim());
        setComment("");
      }}
    >
      <label className={styles.label} htmlFor="progress-comment">
        Add progress comment
      </label>
      <textarea
        className={styles.textarea}
        id="progress-comment"
        onChange={(event) => setComment(event.target.value)}
        placeholder="What changed in this idea?"
        value={comment}
      />

      {error && <p className={styles.error}>{error}</p>}

      <button className={styles.button} disabled={loading} type="submit">
        {loading ? "Saving..." : "Add log"}
      </button>
    </form>
  );
}
