"use client";

import { LoginForm } from "@/modules/auth/components/LoginForm";
import { useLogin } from "@/modules/auth/hooks/useLogin";
import styles from "@/app/login/page.module.scss";

export default function LoginPage() {
  const { loading, error, submit } = useLogin();

  return (
    <main className={styles.page}>
      <LoginForm error={error} loading={loading} onSubmit={submit} />
    </main>
  );
}
