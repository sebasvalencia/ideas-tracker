import { NextRequest, NextResponse } from "next/server";
import { BACKEND_API_V1_BASE_URL } from "@/app/api/_lib/backendApi";

export async function POST(request: NextRequest) {
  const payload = await request.json();

  const response = await fetch(`${BACKEND_API_V1_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    cache: "no-store",
  });

  const raw = await response.text();
  let body: unknown = null;
  if (raw) {
    try {
      body = JSON.parse(raw);
    } catch {
      body = { detail: raw };
    }
  }

  if (!response.ok) {
    const detail =
      typeof body === "object" && body !== null && "detail" in body ? String((body as { detail: unknown }).detail) : "Login failed";
    return NextResponse.json(
      {
        detail,
      },
      { status: response.status },
    );
  }

  return NextResponse.json(body, { status: response.status });
}
