import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { LoginForm } from "@/modules/auth/components/LoginForm";

describe("LoginForm", () => {
  it("shows validation error when fields are empty", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm loading={false} onSubmit={onSubmit} />);

    await user.click(screen.getByRole("button", { name: "Sign in" }));

    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByText("Email and password are required")).toBeTruthy();
  });

  it("calls onSubmit with trimmed email when valid", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm loading={false} onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText("Email"), "  admin@ideas.com  ");
    await user.type(screen.getByLabelText("Password"), "ChangeMe123!");
    await user.click(screen.getByRole("button", { name: "Sign in" }));

    expect(onSubmit).toHaveBeenCalledWith("admin@ideas.com", "ChangeMe123!");
  });
});
