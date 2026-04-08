import { NextRequest, NextResponse } from "next/server";
import { BACKEND_API_V1_BASE_URL } from "@/app/api/_lib/backendApi";

function authHeader(request: NextRequest): string | null {
  const value = request.headers.get("authorization");
  return value ?? null;
}

export async function GET(request: NextRequest) {
  const authorization = authHeader(request);

  const response = await fetch(`${BACKEND_API_V1_BASE_URL}/ideas${request.nextUrl.search}`, {
    method: "GET",
    headers: authorization ? { Authorization: authorization } : {},
    cache: "no-store",
  });

  const raw = await response.text();
  const body = raw ? JSON.parse(raw) : null;
  return NextResponse.json(body, { status: response.status });
}

export async function POST(request: NextRequest) {
  const authorization = authHeader(request);
  const payload = await request.json();

  const response = await fetch(`${BACKEND_API_V1_BASE_URL}/ideas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(authorization ? { Authorization: authorization } : {}),
    },
    body: JSON.stringify(payload),
    cache: "no-store",
  });

  const raw = await response.text();
  const body = raw ? JSON.parse(raw) : null;
  return NextResponse.json(body, { status: response.status });
}
