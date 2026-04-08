"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

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
import { clearAccessToken, getAccessToken } from "@/modules/auth/services/tokenSession";
import { EmptyState } from "@/shared/ui/EmptyState";
import { SkeletonBlock } from "@/shared/ui/SkeletonBlock";

type IdeaStatus = "idea" | "in_progress" | "completed";

export default function IdeaDetailPage() {
  const router = useRouter();
  const params = useParams<{ ideaId: string }>();
  const ideaId = Number(params.ideaId);
  const [token, setToken] = useState<string | null>(null);
  const { idea, loading, error, refresh } = useIdeaDetail(token, Number.isFinite(ideaId) ? ideaId : null);
  const { patchIdea, loading: patchLoading, deleting, removeIdea, error: patchError, clearError } = useIdeaMutations(
    token,
    Number.isFinite(ideaId) ? ideaId : null,
  );
  const {
    logs,
    loading: logsLoading,
    submitting: logSubmitting,
    error: logsError,
    addLog,
  } = useProgressLogs(token, Number.isFinite(ideaId) ? ideaId : null);
  const [draftStatus, setDraftStatus] = useState<IdeaStatus | null>(null);
  const [draftProgress, setDraftProgress] = useState<number | null>(null);
  const [localValidation, setLocalValidation] = useState<string | null>(null);

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

  useEffect(() => {
    setToken(getAccessToken());
  }, []);

  const combinedError = useMemo(
    () => localValidation ?? patchError ?? logsError ?? ratingError ?? error,
    [error, localValidation, logsError, patchError, ratingError],
  );

  async function handleSave() {
    clearError();
    setLocalValidation(null);

    const normalizedProgress = Math.max(0, Math.min(100, Number(progress)));
    if (status === "completed" && normalizedProgress !== 100) {
      setLocalValidation("Completed status requires progress at 100%");
      return;
    }

    const updated = await patchIdea({
      status,
      execution_percentage: normalizedProgress,
    });

    if (updated) {
      setDraftStatus((updated.status as IdeaStatus) ?? "idea");
      setDraftProgress(updated.execution_percentage);
      await refresh();
    }
  }

  function handleLogout() {
    clearAccessToken();
    router.replace("/login");
  }

  function handleBackToIdeas() {
    router.push("/ideas");
  }

  async function handleDelete() {
    if (!idea) {
      return;
    }
    const confirmed = window.confirm("Delete this idea? This action cannot be undone.");
    if (!confirmed) {
      return;
    }
    const deleted = await removeIdea();
    if (deleted) {
      router.replace("/ideas");
    }
  }

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <div className={styles.headerTop}>
          <h1 className={styles.title}>Idea detail</h1>
          <div className={styles.headerActions}>
            <button className={styles.secondaryButton} onClick={handleBackToIdeas} type="button">
              Back to ideas
            </button>
            <button className={styles.logoutButton} onClick={handleLogout} type="button">
              Logout
            </button>
          </div>
        </div>
        <p className={styles.subtitle}>ID: {ideaId}</p>
      </header>

      {loading && (
        <section className={styles.card} aria-label="Loading detail">
          <SkeletonBlock size="lg" />
          <SkeletonBlock size="xl" />
          <SkeletonBlock size="md" />
          <SkeletonBlock size="xl" />
          <SkeletonBlock size="md" />
        </section>
      )}

      {idea && (
        <>
          <section className={styles.card}>
            <div className={styles.row}>
              <span className={styles.label}>Title</span>
              <input className={styles.input} readOnly value={idea.title} />
            </div>

            <div className={styles.row}>
              <span className={styles.label}>Description</span>
              <textarea className={styles.input} readOnly value={idea.description} />
            </div>

            <div className={styles.row}>
              <span className={styles.label}>Current status</span>
              <IdeaStatusBadge status={idea.status} />
            </div>

            <ExecutionProgressBar value={progress} />

            <div className={styles.row}>
              <span className={styles.label}>Update status</span>
              <select className={styles.input} onChange={(event) => setDraftStatus(event.target.value as IdeaStatus)} value={status}>
                <option value="idea">Idea</option>
                <option value="in_progress">In progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div className={styles.row}>
              <span className={styles.label}>Update progress (%)</span>
              <input
                className={styles.input}
                max={100}
                min={0}
                onChange={(event) => setDraftProgress(Number(event.target.value))}
                type="number"
                value={progress}
              />
            </div>

            <div className={styles.actions}>
              <button className={styles.button} disabled={patchLoading || deleting} onClick={handleSave} type="button">
                {patchLoading ? "Saving..." : "Save changes"}
              </button>
              <button className={styles.deleteButton} disabled={patchLoading || deleting} onClick={handleDelete} type="button">
                {deleting ? "Deleting..." : "Delete idea"}
              </button>
            </div>
          </section>

          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Progress logs</h2>
            <ProgressLogTextarea loading={logSubmitting} onSubmit={addLog} />
            {logsLoading ? (
              <div className={styles.loadingStack}>
                <SkeletonBlock size="xl" />
                <SkeletonBlock size="xl" />
              </div>
            ) : (
              <ProgressLogTimeline logs={logs} />
            )}
          </section>

          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Final rating</h2>
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
          </section>
        </>
      )}

      {!loading && !idea && !combinedError && (
        <EmptyState
          description="The idea may have been deleted or you may not have access."
          title="Idea not available"
        />
      )}

      {combinedError && <p className={styles.error}>{combinedError}</p>}
    </main>
  );
}
