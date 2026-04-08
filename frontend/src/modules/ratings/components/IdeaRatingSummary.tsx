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
      <p className={styles.value}>{rating.rating} / 10</p>
      {rating.summary && <p className={styles.text}>{rating.summary}</p>}
    </div>
  );
}
