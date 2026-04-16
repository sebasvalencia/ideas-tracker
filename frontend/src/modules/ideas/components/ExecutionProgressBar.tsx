import styles from "@/modules/ideas/components/ExecutionProgressBar.module.scss";

const STATUS_COLOR: Record<string, string> = {
  idea: "#3b82f6",
  in_progress: "#f97316",
  completed: "#22c55e",
};

type ExecutionProgressBarProps = {
  value: number;
  status?: string;
};

export function ExecutionProgressBar({ value, status = "idea" }: ExecutionProgressBarProps) {
  const normalized = Math.max(0, Math.min(100, value));
  const color = STATUS_COLOR[status] ?? STATUS_COLOR.idea;

  return (
    <div className={styles.wrapper}>
      <div className={styles.labelRow}>
        <span>Execution progress</span>
        <span className={styles.percent}>{normalized}%</span>
      </div>
      <div className={styles.track} role="progressbar" aria-valuenow={normalized} aria-valuemin={0} aria-valuemax={100}>
        <div
          className={styles.fill}
          style={{ width: `${normalized}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}
