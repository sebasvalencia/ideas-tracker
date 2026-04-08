"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import styles from "@/modules/auth/components/PrivateRouteGuard.module.scss";
import { clearAccessToken, hasValidAccessToken } from "@/modules/auth/services/tokenSession";

type PrivateRouteGuardProps = {
  children: React.ReactNode;
};

export function PrivateRouteGuard({ children }: PrivateRouteGuardProps) {
  const router = useRouter();
  const [checking, setChecking] = useState(true);
  const [allowed, setAllowed] = useState(false);

  useEffect(() => {
    const valid = hasValidAccessToken();
    if (!valid) {
      clearAccessToken();
      router.replace("/login");
      setAllowed(false);
      setChecking(false);
      return;
    }
    setAllowed(true);
    setChecking(false);
  }, [router]);

  if (checking) {
    return (
      <div className={styles.wrapper}>
        <p className={styles.message}>Checking session...</p>
      </div>
    );
  }

  if (!allowed) {
    return null;
  }

  return <>{children}</>;
}
