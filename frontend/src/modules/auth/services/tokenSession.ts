export const ACCESS_TOKEN_KEY = "ideas_tracker_access_token";

function readTokenPayload(token: string): { exp?: number; sub?: string; email?: string } | null {
  const parts = token.split(".");
  if (parts.length < 2) {
    return null;
  }
  try {
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const payload = JSON.parse(atob(base64)) as { exp?: number };
    return payload;
  } catch {
    return null;
  }
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function clearAccessToken(): void {
  if (typeof window === "undefined") {
    return;
  }
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export function getTokenEmail(): string | null {
  const token = getAccessToken();
  if (!token) return null;
  const payload = readTokenPayload(token);
  return payload?.email ?? null;
}

export function hasValidAccessToken(): boolean {
  const token = getAccessToken();
  if (!token) {
    return false;
  }
  const payload = readTokenPayload(token);
  if (!payload?.exp) {
    return true;
  }
  const nowInSeconds = Math.floor(Date.now() / 1000);
  return payload.exp > nowInSeconds;
}
