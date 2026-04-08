import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import IdeasPage from "@/app/ideas/page";
import { getAccessToken } from "@/modules/auth/services/tokenSession";
import { useIdeasList } from "@/modules/ideas/hooks/useIdeasList";
import { deleteIdea } from "@/modules/ideas/services/ideasApi";

const replaceMock = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    replace: replaceMock,
  }),
}));

vi.mock("@/modules/auth/services/tokenSession", () => ({
  getAccessToken: vi.fn(),
  clearAccessToken: vi.fn(),
}));

vi.mock("@/modules/ideas/services/ideasApi", () => ({
  createIdea: vi.fn(),
  deleteIdea: vi.fn(),
}));

vi.mock("@/modules/ideas/hooks/useIdeasList", () => ({
  useIdeasList: vi.fn(),
}));

vi.mock("@/modules/ideas/components/IdeaForm", () => ({
  IdeaForm: () => <div>Idea form</div>,
}));

vi.mock("@/modules/ideas/components/IdeaCard", () => ({
  IdeaCard: ({ idea, onDelete, deleting }: { idea: { title: string }; onDelete?: (idea: { title: string }) => void; deleting?: boolean }) => (
    <article>
      <p>{idea.title}</p>
      <button disabled={deleting} onClick={() => onDelete?.(idea)} type="button">
        {deleting ? "Deleting..." : "Delete"}
      </button>
    </article>
  ),
}));

describe("IdeasPage delete modal", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(getAccessToken).mockReturnValue("token");
    vi.mocked(useIdeasList).mockReturnValue({
      ideas: [
        {
          id: 10,
          owner_id: 1,
          title: "Idea A",
          description: "Desc A",
          status: "idea",
          execution_percentage: 0,
          created_at: "2026-01-01T00:00:00Z",
          updated_at: "2026-01-01T00:00:00Z",
          deleted_at: null,
        },
      ],
      loading: false,
      error: null,
      refresh: vi.fn(),
    });
  });

  it("opens delete modal and closes with Escape", async () => {
    const user = userEvent.setup();
    render(<IdeasPage />);

    await user.click(screen.getByRole("button", { name: "Delete" }));
    expect(screen.getByRole("dialog")).toBeTruthy();
    expect(screen.getAllByText("Delete idea").length).toBeGreaterThan(0);

    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).toBeNull();
    });
  });

  it("deletes idea when confirming modal", async () => {
    const user = userEvent.setup();
    const refresh = vi.fn();
    vi.mocked(useIdeasList).mockReturnValue({
      ideas: [
        {
          id: 10,
          owner_id: 1,
          title: "Idea A",
          description: "Desc A",
          status: "idea",
          execution_percentage: 0,
          created_at: "2026-01-01T00:00:00Z",
          updated_at: "2026-01-01T00:00:00Z",
          deleted_at: null,
        },
      ],
      loading: false,
      error: null,
      refresh,
    });
    vi.mocked(deleteIdea).mockResolvedValue();

    render(<IdeasPage />);
    await user.click(screen.getByRole("button", { name: "Delete" }));
    await user.click(screen.getByRole("button", { name: "Delete idea" }));

    await waitFor(() => {
      expect(deleteIdea).toHaveBeenCalledWith("token", 10);
    });
    expect(refresh).toHaveBeenCalled();
  });
});
