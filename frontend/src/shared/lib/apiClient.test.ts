import { requestJson } from "@/shared/lib/apiClient";

describe("apiClient", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("adds bearer token header and parses json response", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    const data = await requestJson<{ ok: boolean }>("/api/demo", {
      token: "abc123",
    });

    expect(data.ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/demo",
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer abc123",
        }),
      }),
    );
  });

  it("throws ApiClientError with backend detail", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ detail: "Unauthorized" }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await expect(requestJson("/api/secure")).rejects.toMatchObject({
      name: "ApiClientError",
      status: 401,
      message: "Unauthorized",
    });
  });
});
