"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { IdeaCard } from "@/modules/ideas/components/IdeaCard";
import { IdeaForm } from "@/modules/ideas/components/IdeaForm";
import { clearAccessToken, getAccessToken } from "@/modules/auth/services/tokenSession";
import { useIdeasList } from "@/modules/ideas/hooks/useIdeasList";
import type { Idea } from "@/modules/ideas/model/idea.types";
import { createIdea, deleteIdea } from "@/modules/ideas/services/ideasApi";
import styles from "@/app/ideas/page.module.scss";
import { EmptyState } from "@/shared/ui/EmptyState";
import { SkeletonBlock } from "@/shared/ui/SkeletonBlock";

export default function IdeasPage() {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [createLoading, setCreateLoading] = useState(false);
  const [deletingIdeaId, setDeletingIdeaId] = useState<number | null>(null);
  const [ideaToDelete, setIdeaToDelete] = useState<Idea | null>(null);
  const [createError, setCreateError] = useState<string | null>(null);
  const { ideas, loading, error, refresh } = useIdeasList(token);

  const sortedIdeas = useMemo(() => ideas, [ideas]);

  useEffect(() => {
    setToken(getAccessToken());
  }, []);

  useEffect(() => {
    if (!ideaToDelete) {
      return;
    }
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape" && deletingIdeaId === null) {
        setIdeaToDelete(null);
      }
    };
    window.addEventListener("keydown", handleEscape);
    return () => {
      window.removeEventListener("keydown", handleEscape);
    };
  }, [ideaToDelete, deletingIdeaId]);

  async function handleCreateIdea(title: string, description: string) {
    if (!token) {
      return;
    }
    setCreateLoading(true);
    setCreateError(null);
    try {
      await createIdea(token, { title, description });
      await refresh();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create idea";
      setCreateError(message);
    } finally {
      setCreateLoading(false);
    }
  }

  function handleLogout() {
    clearAccessToken();
    router.replace("/login");
  }

  function handleDeleteIdeaRequest(idea: Idea) {
    setIdeaToDelete(idea);
    setCreateError(null);
  }

  async function handleConfirmDeleteIdea() {
    if (!token || !ideaToDelete) {
      return;
    }
    setDeletingIdeaId(ideaToDelete.id);
    setCreateError(null);
    try {
      await deleteIdea(token, ideaToDelete.id);
      await refresh();
      setIdeaToDelete(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete idea";
      setCreateError(message);
    } finally {
      setDeletingIdeaId(null);
    }
  }

  function handleDeleteIdea(idea: Idea) {
    if (!token) {
      return;
    }
    handleDeleteIdeaRequest(idea);
  }

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <div className={styles.headerTop}>
          <h1 className={styles.title}>Ideas</h1>
          <button className={styles.logoutButton} onClick={handleLogout} type="button">
            Logout
          </button>
        </div>
        <p className={styles.subtitle}>Track progress, logs and final rating of your projects.</p>
      </header>

      <section className={styles.formSection}>
        <h2 className={styles.sectionTitle}>Create new idea</h2>
        <IdeaForm loading={createLoading} onSubmit={handleCreateIdea} />
      </section>
      {createError && <p className={styles.error}>{createError}</p>}

      {error && <p className={styles.error}>{error}</p>}
      <h2 className={styles.sectionTitle}>Ideas list</h2>

      {!loading && !error && sortedIdeas.length === 0 && (
        <EmptyState
          description="Use the form above to register your first idea and start tracking execution."
          title="No ideas yet"
        />
      )}

      {loading && (
        <section className={styles.grid} aria-label="Loading ideas">
          {Array.from({ length: 4 }).map((_, index) => (
            <article className={styles.skeletonCard} key={`idea-skeleton-${index}`}>
              <SkeletonBlock size="lg" />
              <SkeletonBlock size="sm" />
              <SkeletonBlock size="xl" />
              <SkeletonBlock size="md" />
            </article>
          ))}
        </section>
      )}

      {!loading && <section className={styles.grid}>
        {sortedIdeas.map((idea) => (
          <IdeaCard
            deleting={deletingIdeaId === idea.id}
            idea={idea}
            key={idea.id}
            onDelete={handleDeleteIdea}
          />
        ))}
      </section>}

      {ideaToDelete && (
        <div
          className={styles.modalOverlay}
          onClick={(event) => {
            if (event.target === event.currentTarget && deletingIdeaId === null) {
              setIdeaToDelete(null);
            }
          }}
          role="presentation"
        >
          <section aria-modal="true" className={styles.modalCard} role="dialog">
            <h3 className={styles.modalTitle}>Delete idea</h3>
            <p className={styles.modalText}>
              Are you sure you want to delete <strong>{ideaToDelete.title}</strong>? This action cannot be undone.
            </p>
            <div className={styles.modalActions}>
              <button
                className={styles.modalCancel}
                disabled={deletingIdeaId === ideaToDelete.id}
                onClick={() => setIdeaToDelete(null)}
                type="button"
              >
                Cancel
              </button>
              <button
                className={styles.modalDelete}
                disabled={deletingIdeaId === ideaToDelete.id}
                onClick={() => void handleConfirmDeleteIdea()}
                type="button"
              >
                {deletingIdeaId === ideaToDelete.id ? "Deleting..." : "Delete idea"}
              </button>
            </div>
          </section>
        </div>
      )}
    </main>
  );
}
