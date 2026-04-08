import styles from "@/modules/ideas/components/IdeaStatusBadge.module.scss";

type IdeaStatusBadgeProps = {
  status: string;
};

const STATUS_LABEL: Record<string, string> = {
  idea: "Idea",
  in_progress: "In progress",
  completed: "Completed",
};

export function IdeaStatusBadge({ status }: IdeaStatusBadgeProps) {
  const normalized = status in STATUS_LABEL ? status : "idea";
  const className =
    normalized === "in_progress" ? styles.inProgress : normalized === "completed" ? styles.completed : styles.idea;

  return <span className={`${styles.badge} ${className}`}>{STATUS_LABEL[normalized]}</span>;
}
