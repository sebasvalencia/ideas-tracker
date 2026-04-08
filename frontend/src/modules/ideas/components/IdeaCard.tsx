import Link from "next/link";

import { ExecutionProgressBar } from "@/modules/ideas/components/ExecutionProgressBar";
import { IdeaStatusBadge } from "@/modules/ideas/components/IdeaStatusBadge";
import type { Idea } from "@/modules/ideas/model/idea.types";
import styles from "@/modules/ideas/components/IdeaCard.module.scss";

type IdeaCardProps = {
  idea: Idea;
  onDelete?: (idea: Idea) => void;
  deleting?: boolean;
};

export function IdeaCard({ idea, onDelete, deleting = false }: IdeaCardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.header}>
        <h3 className={styles.title}>{idea.title}</h3>
        <IdeaStatusBadge status={idea.status} />
      </div>
      <p className={styles.description}>{idea.description}</p>
      <ExecutionProgressBar value={idea.execution_percentage} />
      <div className={styles.actions}>
        <Link className={styles.link} href={`/ideas/${idea.id}`}>
          View detail
        </Link>
        {onDelete && (
          <button className={styles.deleteButton} disabled={deleting} onClick={() => onDelete(idea)} type="button">
            {deleting ? "Deleting..." : "Delete"}
          </button>
        )}
      </div>
    </article>
  );
}
