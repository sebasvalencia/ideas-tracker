"use client";

import { useRouter } from "next/navigation";
import { useEffect, useSyncExternalStore } from "react";

import styles from "@/modules/auth/components/PrivateRouteGuard.module.scss";
import { clearAccessToken, hasValidAccessToken } from "@/modules/auth/services/tokenSession";

type PrivateRouteGuardProps = {
  children: React.ReactNode;
};

const noopSubscribe = () => () => {};

export function PrivateRouteGuard({ children }: PrivateRouteGuardProps) {
  const router = useRouter();
  const isClient = useSyncExternalStore(noopSubscribe, () => true, () => false);
  const authed = useSyncExternalStore(
    noopSubscribe,
    () => hasValidAccessToken(),
    () => false,
  );

  useEffect(() => {
    if (!isClient || authed) {
      return;
    }
    clearAccessToken();
    router.replace("/login");
  }, [isClient, authed, router]);

  if (!isClient) {
    return (
      <div className={styles.wrapper}>
        <p className={styles.message}>Checking session...</p>
      </div>
    );
  }

  if (!authed) {
    return null;
  }

  return <>{children}</>;
}
