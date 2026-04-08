import { render, screen, waitFor } from "@testing-library/react";

import { PrivateRouteGuard } from "@/modules/auth/components/PrivateRouteGuard";
import { clearAccessToken, hasValidAccessToken } from "@/modules/auth/services/tokenSession";

const replaceMock = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    replace: replaceMock,
  }),
}));

vi.mock("@/modules/auth/services/tokenSession", () => ({
  hasValidAccessToken: vi.fn(),
  clearAccessToken: vi.fn(),
}));

describe("PrivateRouteGuard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders children when session is valid", async () => {
    vi.mocked(hasValidAccessToken).mockReturnValue(true);

    render(
      <PrivateRouteGuard>
        <p>Private content</p>
      </PrivateRouteGuard>,
    );

    await waitFor(() => {
      expect(screen.getByText("Private content")).toBeTruthy();
    });
    expect(replaceMock).not.toHaveBeenCalled();
    expect(clearAccessToken).not.toHaveBeenCalled();
  });

  it("redirects to login and clears token when session is invalid", async () => {
    vi.mocked(hasValidAccessToken).mockReturnValue(false);

    render(
      <PrivateRouteGuard>
        <p>Private content</p>
      </PrivateRouteGuard>,
    );

    await waitFor(() => {
      expect(replaceMock).toHaveBeenCalledWith("/login");
    });
    expect(clearAccessToken).toHaveBeenCalled();
    expect(screen.queryByText("Private content")).toBeNull();
  });
});
