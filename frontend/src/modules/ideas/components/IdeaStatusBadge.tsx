import styles from "@/modules/ideas/components/IdeaStatusBadge.module.scss";

type IdeaStatusBadgeProps = {
  status: string;
};

const STATUS_LABEL: Record<string, string> = {
  idea: "Idea",
  in_progress: "In progress",
  completed: "Completed",
};

const STATUS_DOT_COLOR: Record<string, string> = {
  idea: "#1d4ed8",
  in_progress: "#d97706",
  completed: "#15803d",
};

export function IdeaStatusBadge({ status }: IdeaStatusBadgeProps) {
  const normalized = status in STATUS_LABEL ? status : "idea";
  const badgeClass =
    normalized === "in_progress"
      ? styles.inProgress
      : normalized === "completed"
        ? styles.completed
        : styles.idea;

  return (
    <span className={`${styles.badge} ${badgeClass}`}>
      <span
        aria-hidden="true"
        className={styles.dot}
        style={{ backgroundColor: STATUS_DOT_COLOR[normalized] }}
      />
      {STATUS_LABEL[normalized]}
    </span>
  );
}
