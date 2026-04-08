import styles from "@/app/loading.module.scss";

export default function GlobalLoading() {
  return (
    <main className={styles.container}>
      <span aria-label="Loading application" className={styles.spinner} role="status" />
    </main>
  );
}
