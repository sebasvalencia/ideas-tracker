type ApiErrorPayload = {
  code?: string;
  message?: string;
  detail?: string;
  details?: unknown;
};

export class ApiClientError extends Error {
  status: number;
  code?: string;
  details?: unknown;

  constructor(message: string, status: number, code?: string, details?: unknown) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

type RequestJsonOptions = {
  method?: "GET" | "POST" | "PATCH" | "DELETE";
  token?: string;
  body?: unknown;
  headers?: Record<string, string>;
  cache?: RequestCache;
};

function buildHeaders(options: RequestJsonOptions): HeadersInit {
  const headers: Record<string, string> = {
    ...(options.headers ?? {}),
  };
  if (options.token) {
    headers.Authorization = `Bearer ${options.token}`;
  }
  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  return headers;
}

async function parseError(response: Response): Promise<never> {
  const data = (await response.json().catch(() => null)) as ApiErrorPayload | null;
  const message = data?.message ?? data?.detail ?? `Request failed (${response.status})`;
  throw new ApiClientError(message, response.status, data?.code, data?.details);
}

export async function requestJson<T>(path: string, options: RequestJsonOptions = {}): Promise<T> {
  const response = await fetch(path, {
    method: options.method ?? "GET",
    headers: buildHeaders(options),
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
    cache: options.cache ?? "no-store",
  });

  if (!response.ok) {
    return parseError(response);
  }

  if (response.status === 204) {
    return null as T;
  }

  return (await response.json()) as T;
}
