import type { IdeaRating } from "@/modules/ratings/model/rating.types";
import styles from "@/modules/ratings/components/IdeaRatingSummary.module.scss";

type IdeaRatingSummaryProps = {
  rating: IdeaRating | null;
};

export function IdeaRatingSummary({ rating }: IdeaRatingSummaryProps) {
  if (!rating) {
    return null;
  }

  return (
    <div className={styles.summary}>
      <p className={styles.title}>Current rating</p>
      <div className={styles.starsRow}>
        {Array.from({ length: 10 }, (_, i) => i + 1).map((star) => (
          <span
            aria-hidden="true"
            className={star <= rating.rating ? styles.starFilled : styles.starEmpty}
            key={star}
          >
            ★
          </span>
        ))}
        <span className={styles.value}>{rating.rating}/10</span>
      </div>
      {rating.summary && <p className={styles.text}>{rating.summary}</p>}
    </div>
  );
}
