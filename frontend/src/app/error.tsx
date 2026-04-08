"use client";

import styles from "@/app/error.module.scss";

type ErrorPageProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({ error, reset }: ErrorPageProps) {
  return (
    <main className={styles.container}>
      <section className={styles.card}>
        <h2 className={styles.title}>Something went wrong</h2>
        <p className={styles.message}>{error.message || "Unexpected error in the application."}</p>
        <button className={styles.button} onClick={reset} type="button">
          Try again
        </button>
      </section>
    </main>
  );
}
