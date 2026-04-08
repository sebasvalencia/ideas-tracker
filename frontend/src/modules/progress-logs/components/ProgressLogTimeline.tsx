import styles from "@/modules/progress-logs/components/ProgressLogTimeline.module.scss";
import type { ProgressLog } from "@/modules/progress-logs/model/progressLog.types";

type ProgressLogTimelineProps = {
  logs: ProgressLog[];
};

export function ProgressLogTimeline({ logs }: ProgressLogTimelineProps) {
  if (logs.length === 0) {
    return <p className={styles.empty}>No logs yet.</p>;
  }

  return (
    <div className={styles.timeline}>
      {logs.map((log) => (
        <article className={styles.item} key={log.id}>
          <div className={styles.meta}>
            <span>{new Date(log.created_at).toLocaleString()}</span>
            <span>Author #{log.author_id}</span>
          </div>
          <p className={styles.comment}>{log.comment}</p>
          <p className={styles.snapshot}>
            Snapshot: status={log.status_snapshot} | progress={log.progress_snapshot}%
          </p>
        </article>
      ))}
    </div>
  );
}
