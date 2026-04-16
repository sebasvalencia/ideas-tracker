"use client";

import { useEffect, useMemo, useState, useSyncExternalStore } from "react";
import { useParams, useRouter } from "next/navigation";

import styles from "@/app/ideas/[ideaId]/page.module.scss";
import { ExecutionProgressBar } from "@/modules/ideas/components/ExecutionProgressBar";
import { IdeaStatusBadge } from "@/modules/ideas/components/IdeaStatusBadge";
import { useIdeaDetail } from "@/modules/ideas/hooks/useIdeaDetail";
import { useIdeaMutations } from "@/modules/ideas/hooks/useIdeaMutations";
import { ProgressLogTextarea } from "@/modules/progress-logs/components/ProgressLogTextarea";
import { ProgressLogTimeline } from "@/modules/progress-logs/components/ProgressLogTimeline";
import { useProgressLogs } from "@/modules/progress-logs/hooks/useProgressLogs";
import { IdeaRatingForm } from "@/modules/ratings/components/IdeaRatingForm";
import { IdeaRatingSummary } from "@/modules/ratings/components/IdeaRatingSummary";
import { useIdeaRating } from "@/modules/ratings/hooks/useIdeaRating";
import { getAccessToken } from "@/modules/auth/services/tokenSession";
import { EmptyState } from "@/shared/ui/EmptyState";
import { SkeletonBlock } from "@/shared/ui/SkeletonBlock";

const tokenStoreSubscribe = () => () => {};

type IdeaStatus = "idea" | "in_progress" | "completed";

export default function IdeaDetailPage() {
  const router = useRouter();
  const params = useParams<{ ideaId: string }>();
  const ideaId = Number(params.ideaId);
  const token = useSyncExternalStore(
    tokenStoreSubscribe,
    () => getAccessToken(),
    () => null,
  );

  const { idea, loading, error, refresh } = useIdeaDetail(
    token,
    Number.isFinite(ideaId) ? ideaId : null,
  );
  const {
    patchIdea,
    loading: patchLoading,
    deleting,
    removeIdea,
    error: patchError,
    clearError,
  } = useIdeaMutations(token, Number.isFinite(ideaId) ? ideaId : null);
  const {
    logs,
    loading: logsLoading,
    submitting: logSubmitting,
    error: logsError,
    addLog,
  } = useProgressLogs(token, Number.isFinite(ideaId) ? ideaId : null);

  const [isEditing, setIsEditing] = useState(false);
  const [draftStatus, setDraftStatus] = useState<IdeaStatus | null>(null);
  const [draftProgress, setDraftProgress] = useState<number | null>(null);
  const [localValidation, setLocalValidation] = useState<string | null>(null);
  const autoLogsOpen = !logsLoading && logs.length > 0;
  const [logsOpenExplicit, setLogsOpenExplicit] = useState<boolean | null>(null);
  const logsOpen = logsOpenExplicit !== null ? logsOpenExplicit : autoLogsOpen;
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const status = draftStatus ?? ((idea?.status as IdeaStatus | undefined) ?? "idea");
  const progress = draftProgress ?? idea?.execution_percentage ?? 0;
  const isCompleted = (idea?.status ?? status) === "completed";

  const {
    rating,
    loading: ratingLoading,
    submitting: ratingSubmitting,
    error: ratingError,
    save: saveRating,
  } = useIdeaRating(token, Number.isFinite(ideaId) ? ideaId : null, isCompleted);

  const combinedError = useMemo(
    () => localValidation ?? patchError ?? logsError ?? ratingError ?? error,
    [error, localValidation, logsError, patchError, ratingError],
  );

  useEffect(() => {
    if (!showDeleteConfirm) return;
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape" && !deleting) setShowDeleteConfirm(false);
    }
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [showDeleteConfirm, deleting]);

  async function handleSave() {
    clearError();
    setLocalValidation(null);
    const normalizedProgress = Math.max(0, Math.min(100, Number(progress)));
    if (status === "completed" && normalizedProgress !== 100) {
      setLocalValidation("Completed status requires progress at 100%");
      return;
    }
    const updated = await patchIdea({ status, execution_percentage: normalizedProgress });
    if (updated) {
      setDraftStatus((updated.status as IdeaStatus) ?? "idea");
      setDraftProgress(updated.execution_percentage);
      setIsEditing(false);
      await refresh();
    }
  }

  function handleCancelEdit() {
    setDraftStatus(null);
    setDraftProgress(null);
    setLocalValidation(null);
    clearError();
    setIsEditing(false);
  }

  async function handleDelete() {
    const deleted = await removeIdea();
    if (deleted) {
      router.replace("/ideas");
    }
  }

  return (
    <main className={styles.page}>
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className={styles.breadcrumb}>
        <button
          className={styles.breadcrumbLink}
          onClick={() => router.push("/ideas")}
          type="button"
        >
          Ideas
        </button>
        <span aria-hidden="true" className={styles.breadcrumbSep}>/</span>
        <span className={styles.breadcrumbCurrent}>
          {idea?.title ?? (loading ? "Loading…" : `Idea ${ideaId}`)}
        </span>
      </nav>

      {/* Loading skeleton */}
      {loading && (
        <section aria-label="Loading detail" className={styles.card}>
          <SkeletonBlock size="lg" />
          <SkeletonBlock size="xl" />
          <SkeletonBlock size="md" />
          <SkeletonBlock size="xl" />
          <SkeletonBlock size="md" />
        </section>
      )}

      {idea && (
        <>
          {/* Main card */}
          <section className={styles.card}>
            {/* View header: title + edit button */}
            <div className={styles.cardHeader}>
              <h1 className={styles.ideaTitle}>{idea.title}</h1>
              {!isEditing && (
                <button
                  className={styles.editButton}
                  onClick={() => setIsEditing(true)}
                  type="button"
                >
                  <svg
                    aria-hidden="true"
                    fill="none"
                    height="14"
                    viewBox="0 0 24 24"
                    width="14"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.75"
                    />
                    <path
                      d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5Z"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.75"
                    />
                  </svg>
                  Edit
                </button>
              )}
            </div>

            {/* Description */}
            <p className={styles.ideaDescription}>{idea.description}</p>

            {/* Status + progress */}
            <div className={styles.statusRow}>
              <IdeaStatusBadge status={idea.status} />
              <span className={styles.ideaDate}>
                Updated {new Date(idea.updated_at).toLocaleDateString()}
              </span>
            </div>

            <ExecutionProgressBar status={idea.status} value={progress} />

            {/* Edit form — shown only in edit mode */}
            {isEditing && (
              <div className={styles.editSection}>
                <hr className={styles.divider} />

                <div className={styles.row}>
                  <label className={styles.label} htmlFor="edit-status">
                    Update status
                  </label>
                  <select
                    className={styles.input}
                    id="edit-status"
                    onChange={(event) => setDraftStatus(event.target.value as IdeaStatus)}
                    value={status}
                  >
                    <option value="idea">Idea</option>
                    <option value="in_progress">In progress</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>

                <div className={styles.row}>
                  <label className={styles.label} htmlFor="edit-progress">
                    Update progress (%)
                  </label>
                  <input
                    className={styles.input}
                    id="edit-progress"
                    max={100}
                    min={0}
                    onChange={(event) => setDraftProgress(Number(event.target.value))}
                    type="number"
                    value={progress}
                  />
                </div>

                {localValidation && <p className={styles.error}>{localValidation}</p>}
                {patchError && <p className={styles.error}>{patchError}</p>}

                <div className={styles.editActions}>
                  <button
                    className={styles.saveButton}
                    disabled={patchLoading || deleting}
                    onClick={handleSave}
                    type="button"
                  >
                    {patchLoading ? "Saving…" : "Save changes"}
                  </button>
                  <button
                    className={styles.cancelButton}
                    disabled={patchLoading || deleting}
                    onClick={handleCancelEdit}
                    type="button"
                  >
                    Cancel
                  </button>
                  <button
                    className={styles.deleteButton}
                    disabled={patchLoading || deleting}
                    onClick={() => setShowDeleteConfirm(true)}
                    type="button"
                  >
                    {deleting ? "Deleting…" : "Delete idea"}
                  </button>
                </div>
              </div>
            )}
          </section>

          {/* Progress logs — collapsible */}
          <section className={styles.section}>
            <button
              aria-expanded={logsOpen}
              className={styles.sectionToggle}
              onClick={() =>
                setLogsOpenExplicit((prev) => {
                  const current = prev ?? autoLogsOpen;
                  return !current;
                })
              }
              type="button"
            >
              <span className={styles.sectionTitle}>Progress logs</span>
              <span className={styles.logsBadge}>{logs.length}</span>
              <svg
                aria-hidden="true"
                className={`${styles.chevron} ${logsOpen ? styles.chevronOpen : ""}`}
                fill="none"
                height="14"
                viewBox="0 0 24 24"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M6 9l6 6 6-6"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                />
              </svg>
            </button>

            {logsOpen && (
              <div className={styles.sectionBody}>
                <ProgressLogTextarea loading={logSubmitting} onSubmit={addLog} />
                {logsLoading ? (
                  <div className={styles.loadingStack}>
                    <SkeletonBlock size="xl" />
                    <SkeletonBlock size="xl" />
                  </div>
                ) : (
                  <ProgressLogTimeline logs={logs} />
                )}
                {logsError && <p className={styles.error}>{logsError}</p>}
              </div>
            )}
          </section>

          {/* Final rating — collapsible */}
          <section className={styles.section}>
            <button
              aria-expanded={isCompleted}
              className={styles.sectionToggle}
              onClick={() => {}}
              type="button"
              style={{ cursor: "default" }}
            >
              <span className={styles.sectionTitle}>Final rating</span>
              {rating && (
                <span className={styles.ratingPreview}>
                  {"★".repeat(rating.rating)}{"☆".repeat(10 - rating.rating)}
                  {" "}{rating.rating}/10
                </span>
              )}
            </button>

            <div className={styles.sectionBody}>
              {ratingLoading ? (
                <div className={styles.loadingStack}>
                  <SkeletonBlock size="lg" />
                  <SkeletonBlock size="md" />
                </div>
              ) : (
                <IdeaRatingSummary rating={rating} />
              )}
              <IdeaRatingForm
                currentRating={rating}
                enabled={isCompleted}
                key={`rating-form-${rating?.id ?? "new"}-${isCompleted ? "enabled" : "disabled"}`}
                loading={ratingSubmitting}
                onSubmit={saveRating}
              />
              {ratingError && <p className={styles.error}>{ratingError}</p>}
            </div>
          </section>
        </>
      )}

      {!loading && !idea && !combinedError && (
        <EmptyState
          description="The idea may have been deleted or you may not have access."
          title="Idea not available"
        />
      )}

      {error && <p className={styles.error}>{error}</p>}

      {/* Delete confirmation modal */}
      {showDeleteConfirm && (
        <div
          className={styles.modalOverlay}
          onClick={(e) => {
            if (e.target === e.currentTarget && !deleting) setShowDeleteConfirm(false);
          }}
          role="presentation"
        >
          <section aria-modal="true" className={styles.modalCard} role="dialog">
            <h3 className={styles.modalTitle}>Delete idea</h3>
            <p className={styles.modalText}>
              Are you sure you want to delete <strong>{idea?.title}</strong>? This action cannot be
              undone.
            </p>
            <div className={styles.modalActions}>
              <button
                className={styles.cancelButton}
                disabled={deleting}
                onClick={() => setShowDeleteConfirm(false)}
                type="button"
              >
                Cancel
              </button>
              <button
                className={styles.modalDelete}
                disabled={deleting}
                onClick={() => void handleDelete()}
                type="button"
              >
                {deleting ? "Deleting…" : "Delete idea"}
              </button>
            </div>
          </section>
        </div>
      )}
    </main>
  );
}
