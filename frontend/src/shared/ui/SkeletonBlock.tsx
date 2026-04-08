import styles from "@/shared/ui/SkeletonBlock.module.scss";

type SkeletonBlockProps = {
  size?: "sm" | "md" | "lg" | "xl";
};

export function SkeletonBlock({ size = "md" }: SkeletonBlockProps) {
  return <div className={`${styles.skeleton} ${styles[size]}`} />;
}
