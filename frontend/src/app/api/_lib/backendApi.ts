const BACKEND_ORIGIN = process.env.BACKEND_API_URL ?? "http://127.0.0.1:8000";

export const BACKEND_API_V1_BASE_URL = process.env.BACKEND_API_V1_BASE_URL ?? `${BACKEND_ORIGIN}/api/v1`;
