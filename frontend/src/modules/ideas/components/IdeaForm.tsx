"use client";

import { useState } from "react";
import styles from "@/modules/ideas/components/IdeaForm.module.scss";

type IdeaFormProps = {
  loading: boolean;
  onSubmit: (title: string, description: string) => Promise<void>;
  onCancel?: () => void;
};

export function IdeaForm({ loading, onSubmit, onCancel }: IdeaFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);

  return (
    <form
      className={styles.form}
      onSubmit={async (event) => {
        event.preventDefault();
        if (!title.trim() || !description.trim()) {
          setError("Title and description are required");
          return;
        }
        setError(null);
        await onSubmit(title.trim(), description.trim());
        setTitle("");
        setDescription("");
      }}
    >
      <input
        className={styles.input}
        onChange={(event) => setTitle(event.target.value)}
        placeholder="Idea title"
        value={title}
      />

      <textarea
        className={`${styles.input} ${styles.textarea}`}
        onChange={(event) => setDescription(event.target.value)}
        placeholder="Idea description"
        value={description}
      />

      {error && <p className={styles.error}>{error}</p>}

      <div className={styles.formActions}>
        {onCancel && (
          <button
            className={styles.cancelButton}
            disabled={loading}
            onClick={onCancel}
            type="button"
          >
            Cancel
          </button>
        )}
        <button className={styles.button} disabled={loading} type="submit">
          {loading ? "Creating..." : "Create idea"}
        </button>
      </div>
    </form>
  );
}
