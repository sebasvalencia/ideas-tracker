import { NextRequest, NextResponse } from "next/server";
import { BACKEND_API_V1_BASE_URL } from "@/app/api/_lib/backendApi";

function authHeader(request: NextRequest): string | null {
  return request.headers.get("authorization");
}

type Params = {
  params: Promise<{ ideaId: string }>;
};

export async function GET(request: NextRequest, { params }: Params) {
  const { ideaId } = await params;
  const authorization = authHeader(request);

  const response = await fetch(`${BACKEND_API_V1_BASE_URL}/ideas/${ideaId}/rating`, {
    method: "GET",
    headers: authorization ? { Authorization: authorization } : {},
    cache: "no-store",
  });

  const raw = await response.text();
  const body = raw ? JSON.parse(raw) : null;
  return NextResponse.json(body, { status: response.status });
}

export async function POST(request: NextRequest, { params }: Params) {
  const { ideaId } = await params;
  const authorization = authHeader(request);
  const payload = await request.json();

  const response = await fetch(`${BACKEND_API_V1_BASE_URL}/ideas/${ideaId}/rating`, {
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

export async function PATCH(request: NextRequest, { params }: Params) {
  const { ideaId } = await params;
  const authorization = authHeader(request);
  const payload = await request.json();

  const response = await fetch(`${BACKEND_API_V1_BASE_URL}/ideas/${ideaId}/rating`, {
    method: "PATCH",
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
