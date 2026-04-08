import type { LoginInput, LoginResponse } from "@/modules/auth/model/types";
import { requestJson } from "@/shared/lib/apiClient";

export async function login(payload: LoginInput): Promise<LoginResponse> {
  return requestJson<LoginResponse>("/api/auth/login", {
    method: "POST",
    body: payload,
  });
}
