"use client";

import { useState } from "react";
import styles from "@/modules/auth/components/LoginForm.module.scss";

type LoginFormProps = {
  loading: boolean;
  error?: string | null;
  onSubmit: (email: string, password: string) => void | Promise<void>;
};

export function LoginForm({ loading, error, onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  return (
    <form
      className={styles.form}
      onSubmit={async (event) => {
        event.preventDefault();
        if (!email.trim() || !password.trim()) {
          setValidationError("Email and password are required");
          return;
        }

        setValidationError(null);
        await onSubmit(email.trim(), password);
      }}
    >
      <div>
        <h1 className={styles.title}>Sign in</h1>
        <p className={styles.subtitle}>Access your ideas workspace</p>
      </div>

      <label className={styles.field}>
        <span className={styles.fieldLabel}>Email</span>
        <input
          autoComplete="email"
          className={styles.input}
          name="email"
          onChange={(event) => setEmail(event.target.value)}
          placeholder="admin@ideas.com"
          type="email"
          value={email}
        />
      </label>

      <label className={styles.field}>
        <span className={styles.fieldLabel}>Password</span>
        <input
          autoComplete="current-password"
          className={styles.input}
          name="password"
          onChange={(event) => setPassword(event.target.value)}
          placeholder="********"
          type="password"
          value={password}
        />
      </label>

      {(validationError || error) && (
        <p className={styles.error}>{validationError ?? error}</p>
      )}

      <button
        className={styles.button}
        disabled={loading}
        type="submit"
      >
        {loading ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
