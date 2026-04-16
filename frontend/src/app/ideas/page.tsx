"use client";

import { useEffect, useMemo, useState } from "react";

import { IdeaCard } from "@/modules/ideas/components/IdeaCard";
import { IdeaForm } from "@/modules/ideas/components/IdeaForm";
import { getAccessToken } from "@/modules/auth/services/tokenSession";
import { useIdeasList } from "@/modules/ideas/hooks/useIdeasList";
import type { Idea } from "@/modules/ideas/model/idea.types";
import { createIdea, deleteIdea } from "@/modules/ideas/services/ideasApi";
import styles from "@/app/ideas/page.module.scss";
import { EmptyState } from "@/shared/ui/EmptyState";
import { SkeletonBlock } from "@/shared/ui/SkeletonBlock";

const PAGE_SIZE = 9;

export default function IdeasPage() {
  const [token, setToken] = useState<string | null>(null);
  const [createLoading, setCreateLoading] = useState(false);
  const [deletingIdeaId, setDeletingIdeaId] = useState<number | null>(null);
  const [ideaToDelete, setIdeaToDelete] = useState<Idea | null>(null);
  const [createError, setCreateError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const { ideas, loading, error, refresh } = useIdeasList(token);

  useEffect(() => {
    setToken(getAccessToken());
  }, []);

  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery]);

  useEffect(() => {
    function handleEscape(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      if (showCreateModal && !createLoading) {
        setShowCreateModal(false);
        return;
      }
      if (ideaToDelete && deletingIdeaId === null) {
        setIdeaToDelete(null);
      }
    }
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [showCreateModal, createLoading, ideaToDelete, deletingIdeaId]);

  const filteredIdeas = useMemo(() => {
    if (!searchQuery.trim()) return ideas;
    const q = searchQuery.toLowerCase();
    return ideas.filter(
      (idea) =>
        idea.title.toLowerCase().includes(q) ||
        idea.description.toLowerCase().includes(q),
    );
  }, [ideas, searchQuery]);

  const totalPages = Math.max(1, Math.ceil(filteredIdeas.length / PAGE_SIZE));
  const paginatedIdeas = filteredIdeas.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE,
  );

  async function handleCreateIdea(title: string, description: string) {
    if (!token) return;
    setCreateLoading(true);
    setCreateError(null);
    try {
      await createIdea(token, { title, description });
      await refresh();
      setShowCreateModal(false);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create idea";
      setCreateError(message);
    } finally {
      setCreateLoading(false);
    }
  }

  async function handleConfirmDeleteIdea() {
    if (!token || !ideaToDelete) return;
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
    if (!token) return;
    setIdeaToDelete(idea);
    setCreateError(null);
  }

  return (
    <main className={styles.page}>
      <div className={styles.pageHeader}>
        <div>
          <h1 className={styles.title}>Ideas</h1>
          <p className={styles.subtitle}>Track progress, logs and final rating of your projects.</p>
        </div>
        <button
          className={styles.newIdeaButton}
          onClick={() => {
            setCreateError(null);
            setShowCreateModal(true);
          }}
          type="button"
        >
          <svg
            aria-hidden="true"
            fill="none"
            height="16"
            viewBox="0 0 24 24"
            width="16"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12 5v14M5 12h14"
              stroke="currentColor"
              strokeLinecap="round"
              strokeWidth="2"
            />
          </svg>
          New idea
        </button>
      </div>

      {!loading && ideas.length > 0 && (
        <div className={styles.searchRow}>
          <div className={styles.searchInputWrapper}>
            <svg
              aria-hidden="true"
              className={styles.searchIcon}
              fill="none"
              height="15"
              viewBox="0 0 24 24"
              width="15"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="1.75" />
              <path
                d="m21 21-4.35-4.35"
                stroke="currentColor"
                strokeLinecap="round"
                strokeWidth="1.75"
              />
            </svg>
            <input
              className={styles.searchInput}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search ideas..."
              type="search"
              value={searchQuery}
            />
          </div>
          <span className={styles.resultsCount}>
            {filteredIdeas.length} {filteredIdeas.length === 1 ? "idea" : "ideas"}
          </span>
        </div>
      )}

      {createError && <p className={styles.error}>{createError}</p>}
      {error && <p className={styles.error}>{error}</p>}

      {!loading && !error && ideas.length === 0 && (
        <EmptyState
          description="Use the button above to register your first idea and start tracking execution."
          title="No ideas yet"
        />
      )}

      {!loading && ideas.length > 0 && filteredIdeas.length === 0 && (
        <EmptyState
          description={`No ideas match "${searchQuery}"`}
          title="No results found"
        />
      )}

      {loading && (
        <section aria-label="Loading ideas" className={styles.grid}>
          {Array.from({ length: 6 }).map((_, index) => (
            <article className={styles.skeletonCard} key={`idea-skeleton-${index}`}>
              <SkeletonBlock size="lg" />
              <SkeletonBlock size="sm" />
              <SkeletonBlock size="xl" />
              <SkeletonBlock size="md" />
            </article>
          ))}
        </section>
      )}

      {!loading && paginatedIdeas.length > 0 && (
        <section className={styles.grid}>
          {paginatedIdeas.map((idea) => (
            <IdeaCard
              deleting={deletingIdeaId === idea.id}
              idea={idea}
              key={idea.id}
              onDelete={handleDeleteIdea}
            />
          ))}
        </section>
      )}

      {!loading && totalPages > 1 && (
        <div className={styles.pagination}>
          <button
            className={styles.pageButton}
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => p - 1)}
            type="button"
          >
            ← Prev
          </button>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
            <button
              className={`${styles.pageButton} ${page === currentPage ? styles.pageButtonActive : ""}`}
              key={page}
              onClick={() => setCurrentPage(page)}
              type="button"
            >
              {page}
            </button>
          ))}
          <button
            className={styles.pageButton}
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => p + 1)}
            type="button"
          >
            Next →
          </button>
        </div>
      )}

      {showCreateModal && (
        <div
          className={styles.modalOverlay}
          onClick={(event) => {
            if (event.target === event.currentTarget && !createLoading) {
              setShowCreateModal(false);
            }
          }}
          role="presentation"
        >
          <section aria-modal="true" className={styles.modalCard} role="dialog">
            <h2 className={styles.modalTitle}>New idea</h2>
            <p className={styles.modalText}>
              Fill in the details to add a new idea to your tracker.
            </p>
            <IdeaForm
              loading={createLoading}
              onCancel={() => setShowCreateModal(false)}
              onSubmit={handleCreateIdea}
            />
          </section>
        </div>
      )}

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
              Are you sure you want to delete <strong>{ideaToDelete.title}</strong>? This action
              cannot be undone.
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
