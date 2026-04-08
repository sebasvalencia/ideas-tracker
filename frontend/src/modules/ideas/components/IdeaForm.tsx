"use client";

import { useState } from "react";
import styles from "@/modules/ideas/components/IdeaForm.module.scss";

type IdeaFormProps = {
  loading: boolean;
  onSubmit: (title: string, description: string) => Promise<void>;
};

export function IdeaForm({ loading, onSubmit }: IdeaFormProps) {
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
      <h2 className={styles.title}>Create idea</h2>

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

      <button
        className={styles.button}
        disabled={loading}
        type="submit"
      >
        {loading ? "Creating..." : "Create"}
      </button>
    </form>
  );
}
