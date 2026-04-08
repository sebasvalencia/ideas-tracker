import styles from "@/modules/ideas/components/ExecutionProgressBar.module.scss";

type ExecutionProgressBarProps = {
  value: number;
};

export function ExecutionProgressBar({ value }: ExecutionProgressBarProps) {
  const normalized = Math.max(0, Math.min(100, value));
  return (
    <div className={styles.wrapper}>
      <div className={styles.labelRow}>
        <span>Execution progress</span>
        <span>{normalized}%</span>
      </div>
      <progress className={styles.track} max={100} value={normalized} />
    </div>
  );
}
