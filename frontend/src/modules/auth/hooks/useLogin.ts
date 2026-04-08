"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { login } from "@/modules/auth/services/authApi";
import { ACCESS_TOKEN_KEY } from "@/modules/auth/services/tokenSession";

type UseLoginState = {
  loading: boolean;
  error: string | null;
};

export function useLogin() {
  const router = useRouter();
  const [state, setState] = useState<UseLoginState>({
    loading: false,
    error: null,
  });

  async function submit(email: string, password: string) {
    setState({ loading: true, error: null });
    try {
      const auth = await login({ email, password });
      localStorage.setItem(ACCESS_TOKEN_KEY, auth.access_token);
      router.push("/ideas");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unexpected error";
      setState({ loading: false, error: message });
      return;
    }
    setState({ loading: false, error: null });
  }

  return {
    loading: state.loading,
    error: state.error,
    submit,
  };
}
