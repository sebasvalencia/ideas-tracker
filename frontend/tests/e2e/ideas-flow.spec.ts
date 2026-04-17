import { expect, test } from "@playwright/test";

const E2E_EMAIL = process.env.E2E_EMAIL || "admin@ideas.com";
const E2E_PASSWORD = process.env.E2E_PASSWORD || "ChangeMe123!";

test("login, create idea, update, add log and rate", async ({ page }) => {
  test.setTimeout(60_000);
  const uniqueTitle = `E2E Idea ${Date.now()}`;

  await page.goto("/login");
  await page.getByLabel("Email").fill(E2E_EMAIL);
  await page.getByLabel("Password").fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();

  // Argon2 + JWT + Next.js navigation can take several seconds in CI — wait for URL first.
  await page.waitForURL("**/ideas", { timeout: 15_000 });
  await expect(page.getByRole("heading", { level: 1, name: "Ideas", exact: true })).toBeVisible();

  await page.getByRole("button", { name: "New idea" }).click();
  const createDialog = page.getByRole("dialog");
  await expect(createDialog.getByPlaceholder("Idea title")).toBeVisible();

  await createDialog.getByPlaceholder("Idea title").fill(uniqueTitle);
  await createDialog.getByPlaceholder("Idea description").fill("E2E flow description");
  await createDialog.getByRole("button", { name: "Create idea" }).click();

  await expect(page.getByText(uniqueTitle)).toBeVisible();
  await page.locator("article", { hasText: uniqueTitle }).getByRole("link", { name: "View detail" }).click();

  await expect(page.getByRole("heading", { level: 1, name: uniqueTitle })).toBeVisible();
  await page.getByRole("button", { name: "Edit" }).click();
  await page.getByLabel("Update status").selectOption("completed");
  await page.getByLabel("Update progress (%)").fill("100");
  await page.getByRole("button", { name: "Save changes" }).click();

  // With no logs yet, the progress block stays collapsed until expanded.
  await page.getByRole("button", { name: /Progress logs/i }).click();
  await page.getByLabel("Add progress comment").fill("E2E progress log");
  await page.getByRole("button", { name: "Add log" }).click();
  await expect(page.getByText("E2E progress log")).toBeVisible();

  await page.getByRole("button", { name: "Rate 9 out of 10" }).click();
  await page.getByLabel("Summary").fill("Excellent outcome");
  await page.getByRole("button", { name: "Save rating" }).click();
  await expect(page.getByText("Current rating", { exact: true })).toBeVisible();
  await expect(
    page.getByText("Current rating", { exact: true }).locator("..").getByText("9/10", { exact: true }),
  ).toBeVisible();
});
