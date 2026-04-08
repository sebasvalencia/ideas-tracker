import { act, renderHook } from "@testing-library/react";

import { useIdeaMutations } from "@/modules/ideas/hooks/useIdeaMutations";
import { deleteIdea, updateIdea } from "@/modules/ideas/services/ideasApi";

vi.mock("@/modules/ideas/services/ideasApi", () => ({
  updateIdea: vi.fn(),
  deleteIdea: vi.fn(),
}));

describe("useIdeaMutations", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("updates an idea successfully", async () => {
    const updated = {
      id: 1,
      owner_id: 1,
      title: "Updated",
      description: "Desc",
      status: "in_progress",
      execution_percentage: 40,
      created_at: "2026-01-01T00:00:00Z",
      updated_at: "2026-01-01T00:00:00Z",
      deleted_at: null,
    };
    vi.mocked(updateIdea).mockResolvedValue(updated);

    const { result } = renderHook(() => useIdeaMutations("token", 1));
    let response = null;
    await act(async () => {
      response = await result.current.patchIdea({ status: "in_progress", execution_percentage: 40 });
    });

    expect(updateIdea).toHaveBeenCalledWith("token", 1, { status: "in_progress", execution_percentage: 40 });
    expect(response).toEqual(updated);
    expect(result.current.error).toBeNull();
  });

  it("stores error when update fails", async () => {
    vi.mocked(updateIdea).mockRejectedValue(new Error("Patch failed"));
    const { result } = renderHook(() => useIdeaMutations("token", 1));

    await act(async () => {
      await result.current.patchIdea({ status: "completed", execution_percentage: 100 });
    });

    expect(result.current.error).toBe("Patch failed");
  });

  it("returns false for delete when token or idea is missing", async () => {
    const { result } = renderHook(() => useIdeaMutations(null, null));

    let deleted = true;
    await act(async () => {
      deleted = await result.current.removeIdea();
    });

    expect(deleted).toBe(false);
    expect(deleteIdea).not.toHaveBeenCalled();
  });

  it("deletes idea successfully", async () => {
    vi.mocked(deleteIdea).mockResolvedValue();
    const { result } = renderHook(() => useIdeaMutations("token", 99));

    let deleted = false;
    await act(async () => {
      deleted = await result.current.removeIdea();
    });

    expect(deleteIdea).toHaveBeenCalledWith("token", 99);
    expect(deleted).toBe(true);
    expect(result.current.deleting).toBe(false);
  });
});
